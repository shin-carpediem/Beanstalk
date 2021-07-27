from restaurant.views import order_status_ch
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Sum
from itertools import chain
import time
import customer.models
from webpush import send_user_notification
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice
from account.models import User, nonLoginUser
from restaurant.models import Allergy, Category, Menu, Nomiho


# Create your views here.
# TODO: 要確認
def stop_nomiho(request, duration):
    uuid = request.session['nonloginuser_uuid']
    user_uuid = nonLoginUser.objects.get(uuid=uuid)

    time.sleep(int(duration)*60)
    user_uuid.nomiho = False
    user_uuid.save()
    print("ok!!")


def index(request):
    return render(request, 'customer/index.html')


def table(request):
    user = request.user

    # 新規/既存をセッションで判断する
    # 新規
    if not request.session['nonloginuser_uuid']:

        if user.is_authenticated:
            return redirect('restaurant:logout')
        else:
            return render(request, 'customer/table.html')
    # 既存
    else:
        return redirect('customer:menu')


def menu(request):
    user = request.user

    categories = Category.objects.defer('created_at').order_by('id')
    allergies = Allergy.objects.all().order_by('id')

    restaurant_name = None
    restaurant_logo = None
    try:
        restaurant = User.objects.get(id=1)
        restaurant_name = restaurant.name
        restaurant_logo = restaurant.logo.url
    except Exception:
        pass
    try:
        restaurant = User.objects.get(id=2)
        restaurant_name = restaurant.name
        restaurant_logo = restaurant.logo.url
    except Exception:
        pass
    try:
        restaurant = User.objects.get(id=3)
        restaurant_name = restaurant.name
        restaurant_logo = restaurant.logo.url
    except Exception:
        pass

    if user.is_authenticated:
        table_num = '管理者'
    else:

        # 新規の客かどうかをセッションで判断する
        # 新規
        if not request.session['nonloginuser_uuid']:
            table_num = request.GET.get('table')

            try:
                newuser = nonLoginUser(table=table_num, active=True)
                newuser.save()

            except Exception:
                messages.info(request, f'申し訳ございません。エラーが発生しました。')
                return redirect('customer:index')

            uuid = str(newuser.uuid)

            # レストラン名のセッションを作成
            request.session['restaurant_name'] = restaurant_name
            # レストランのロゴのセッションを作成
            request.session['restaurant_logo'] = restaurant_logo
            # テーブル番号のセッションを作成
            request.session['table'] = table_num
            # uuidのセッションを作成
            request.session['nonloginuser_uuid'] = uuid
        # 既存
        else:

            try:
                uuid = request.session['nonloginuser_uuid']
            except Exception:
                messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
                return redirect('customer:table')

            user_uuid = nonLoginUser.objects.get(uuid=uuid)

            if user_uuid.active == False:
                return redirect('customer:thanks')

    try:
        category = request.session['category_name']
    # カテゴリーセッションがない場合（つまり一番最初に訪れた時）は、一番最初のカテゴリーのページとする
    except Exception:
        category = categories[0].id
        # カテゴリーIDのセッションを作成
        request.session['category_name'] = category

    menus = Menu.objects.defer('created_at').filter(
        category=category).order_by('-id')

    ctx = {
        'categories': categories,
        'menus': menus,
        'allergies': allergies,
        'user_uuid': user_uuid,
    }

    return render(request, 'customer/menu.html', ctx)


def filter(request):
    user = request.user
    # 店側から
    if user.is_authenticated:
        None
    # 客側から
    else:

        try:
            uuid = request.session['nonloginuser_uuid']
        except Exception:
            messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
            return redirect('customer:table')

    try:
        category = request.GET.get('category_name')
        category_id = Category.objects.get(name=category)

        # カテゴリーのセッションを更新
        request.session['category_name'] = category_id.id
        menus = Menu.objects.defer('created_at').filter(
            category=category_id).order_by('-id')
    except Exception:
        menus = None

    try:
        user_uuid = nonLoginUser.objects.get(uuid=uuid)

        if user_uuid.active == False:
            return redirect('customer:thanks')

    # まだ1人もお客さんが使用していない初期設定時を想定
    except Exception:
        user_uuid = None

    categories = Category.objects.defer('created_at').order_by('id')
    allergies = Allergy.objects.defer('created_at').order_by('id')

    ctx = {
        'categories': categories,
        'menus': menus,
        'allergies': allergies,
        'user_uuid': user_uuid,
    }

    # 飲み放題のカテゴリーを選択した場合
    if category_id.nomiho == True:
        nomihos = Nomiho.objects.defer('created_at').order_by('-id')
        ctx['nomihos'] = nomihos
        ctx['nomiho_category'] = "Yes"
        messages.info(request, f'このページのメニューは飲み放題を開始すると注文できます')
    else:
        ctx['nomiho_category'] = "No"

    return render(request, 'customer/menu.html', ctx)


def menu_detail(request, menu_id):
    user = request.user
    if user.is_authenticated:
        None
    else:

        try:
            request.session['nonloginuser_uuid']
        except Exception:
            messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
            return redirect('customer:table')

    menu = get_object_or_404(Menu, pk=menu_id)

    allergies = Allergy.objects.defer('created_at').order_by('id')
    has_allergies = menu.allergies.all().order_by('id')

    ctx = {
        'menu': menu,
        'allergies': allergies,
        'has_allergies': has_allergies,
        'add_cart': "direct",
    }

    return render(request, 'customer/detail.html', ctx)


@require_POST
def cart(request):
    try:
        uuid = request.session['nonloginuser_uuid']
    except Exception:
        messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
        return redirect('customer:table')

    user_uuid = nonLoginUser.objects.get(uuid=uuid)
    user_table = user_uuid.table
    same_table_user_list = nonLoginUser.objects.defer(
        'created_at').filter(table=user_table, active=True)
    same_table_cart_list = ''

    for same_table_user in same_table_user_list:
        same_table_cart = customer.models.Cart.objects.defer(
            'created_at').filter(customer=same_table_user, curr=True).order_by('-id')
        same_table_cart_list = list(
            chain(same_table_cart_list, same_table_cart))

    if user_uuid.active == False:
        return redirect('customer:thanks')

    # Cartデータの保存
    menu_id = request.POST.get('menu_id')
    cart_num = request.POST.get('cart_num')
    menu_instance = Menu.objects.get(id=menu_id)

    # すでにカートに同じ商品が追加されていないかチェック
    try:
        cart = customer.models.Cart.objects.get(menu=menu_instance, curr=True)
        cart.num += int(cart_num)
    except Exception:
        cart = customer.models.Cart(menu=menu_instance, num=cart_num,
                                    customer=user_uuid, curr=True)

    cart.save()

    return redirect('customer:menu')


def cart_static(request):
    try:
        uuid = request.session['nonloginuser_uuid']
    except Exception:
        messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
        return redirect('customer:table')

    user_uuid = nonLoginUser.objects.get(uuid=uuid)

    if user_uuid.active == False:
        return redirect('customer:thanks')

    carts = ''
    table_num = request.session['table']
    # ユーザーのテーブル番号と同じで、かつactiveステータスのユーザーを抽出
    same_user_table_list = nonLoginUser.objects.defer(
        'created_at').filter(table=table_num, active=True)

    # そのユーザー毎がオーダーした内容をまとめたCartリストを作成
    for same_user in same_user_table_list:
        same_user_carts = customer.models.Cart.objects.defer('created_at').filter(
            customer=same_user.uuid, curr=True).order_by('-id')

        carts = list(chain(carts, same_user_carts))

    ctx = {
        'carts': carts,
    }

    return render(request, 'customer/cart.html', ctx)


def cart_detail(request, menu_id):
    try:
        uuid = request.session['nonloginuser_uuid']
    except Exception:
        messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
        return redirect('customer:table')

    user_uuid = nonLoginUser.objects.get(uuid=uuid)

    if user_uuid.active == False:
        return redirect('customer:thanks')

    num = request.GET.get('num')
    cart_id = request.GET.get('id')
    type = request.GET.get('type')
    menu = get_object_or_404(Menu, pk=menu_id)

    allergies = Allergy.objects.defer('created_at').order_by('id')
    has_allergies = menu.allergies.defer('created_at').order_by('id')

    ctx = {
        'menu': menu,
        'allergies': allergies,
        'has_allergies': has_allergies,
        'num': num,
        'cart_id': cart_id,
    }

    if type == 'history-order':
        tag = "off"
        ctx['tag'] = tag

    return render(request, 'customer/cart_detail.html', ctx)


@require_GET
def cart_ch(request):
    try:
        uuid = request.session['nonloginuser_uuid']
    except Exception:
        messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
        return redirect('customer:table')

    user_uuid = nonLoginUser.objects.get(uuid=uuid)

    if user_uuid.active == False:
        return redirect('customer:thanks')

    cart_id = request.GET.get('cart_id')
    type = request.GET.get('type')

    # Cartデータの更新
    try:
        cart = customer.models.Cart.objects.defer('created_at').get(id=cart_id, curr=True)

        if type == 'change':
            cart_num = request.GET.get('cart_num')
            cart.num = cart_num
            cart.save()
        elif type == 'delete':
            cart.delete()
        else:
            None
    except:
        pass

    carts = ''
    table_num = request.session['table']
    # ユーザーのテーブル番号と同じで、かつactiveステータスのユーザーを抽出
    same_user_table_list = nonLoginUser.objects.defer(
        'created_at').filter(table=table_num, active=True)

    # そのユーザー毎がオーダーした内容をまとめたCartリストを作成
    for same_user in same_user_table_list:
        same_user_carts = customer.models.Cart.objects.defer('created_at').filter(
            customer=same_user.uuid, curr=True).order_by('-id')

        carts = list(chain(carts, same_user_carts))

    ctx = {
        'carts': carts,
    }

    return render(request, 'customer/cart.html', ctx)


def order(request):
    try:
        uuid = request.session['nonloginuser_uuid']
    except Exception:
        messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
        return redirect('customer:table')

    user_uuid = nonLoginUser.objects.get(uuid=uuid)

    if user_uuid.active == False:
        return redirect('customer:thanks')

    try:
        table_num = request.session['table']
        # ユーザーのテーブル番号と同じで、かつactiveステータスのユーザーを抽出
        same_user_table_list = nonLoginUser.objects.defer(
            'created_at').filter(table=table_num, active=True)

        # そのユーザー毎がカートに追加した内容をまとめたCartリストを作成
        for same_user in same_user_table_list:
            same_user_carts = customer.models.Cart.objects.defer('created_at').filter(
                customer=same_user.uuid, curr=True).order_by('-id')

            # 同時に同じテーブルの人が注文した際は後者を弾く為
            if not same_user_carts == None:

                cart_price = 0

                for each in same_user_carts:
                    order = customer.models.Order(status='調理中', menu=each.menu,
                                                  num=each.num, customer=each.customer, curr=True)
                    order.save()
                    cart_price = cart_price + (each.menu.price * each.num)

                same_user.price += int(cart_price)

                same_user_carts.delete()
            else:
                messages.info(request, f"注文を先ほど承っております。")
                return redirect('customer:cart')

        # You can still use .filter() or any methods that return QuerySet (from the chain)
        # device = FCMDevice.objects.all().first()
        user = User.objects.get(id=1)
        try:
            user = User.objects.get(id=2)
        except Exception:
            pass
        try:
            user = User.objects.get(id=3)
        except Exception:
            pass

        payload = {"head": "注文が来ました", "body": "確認してください"}
        send_user_notification(user=user, payload=payload, ttl=1000)

        # device = FCMDevice.objects.filter(user=user_id).first()
        # print("ok")

        # title = 'title'
        # message = 'mess'
        # data = None

        # send_message parameters include: message, dry_run, app
        # device.send_message(notification=Notification(title='title', body='message'))
        # result = device.send_message(title=title, body=message, data=data, sound=True)
        # print(result)
        print("ok")

    except Exception:
        pass

    messages.info(request, f"注文を承りました。今しばらくお待ちください")

    return redirect('customer:menu')


# 飲み放題開始用のボタン
@require_GET
def nomiho(request):
    user = request.user
    if user.is_authenticated:
        return redirect('customer:index')
    else:

        try:
            uuid = request.session['nonloginuser_uuid']
        except Exception:
            messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
            return redirect('customer:table')

        user_uuid = nonLoginUser.objects.get(uuid=uuid)

        if user_uuid.active == False:
            return redirect('customer:thanks')

        nomiho_type = request.GET.get('nomiho_type')

        category_id = request.session['category_name']
        categories = Category.objects.defer('created_at').order_by('id')
        menus = Menu.objects.defer('created_at').filter(
            category=category_id).order_by('-id')
        allergies = Allergy.objects.defer('created_at').order_by('id')

        # 同じテーブルのそれぞれのお客さんの合計金額に加算する。また、飲み放題に関する情報を記述する。
        try:
            nomiho_query = Nomiho.objects.get(id=nomiho_type)

            table_num = request.session['table']
            same_user_table_list = nonLoginUser.objects.defer(
                'created_at').filter(table=table_num, active=True)

            for same_user in same_user_table_list:
                same_user.price += int(nomiho_query.price)
                same_user.save()
                # 各々の「飲み放題」ステータス：yes/noをyesにする
                same_user.nomiho = True
                same_user.save()
                same_user.nomiho_name = nomiho_query.name
                same_user.save()
                same_user.nomiho_price += int(nomiho_query.price)
                same_user.save()

                nomiho_is_started = same_user.nomiho

                # TODO:
                duration = nomiho_query.duration
                stop_nomiho(request, duration)

                messages.info(
                    request, f'🍺 飲み放題を開始しました！！🍶  制限時間は{duration}分です！')

        except Exception:
            nomiho_query = None

        ctx = {
            'categories': categories,
            'menus': menus,
            'allergies': allergies,
            'nomiho_query': nomiho_query,
            'user_uuid': user_uuid,
            'nomiho_is_started': nomiho_is_started,
        }

        return render(request, 'customer/menu.html', ctx)


def history(request):
    try:
        uuid = request.session['nonloginuser_uuid']
    except Exception:
        messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
        return redirect('customer:table')

    user_uuid = nonLoginUser.objects.get(uuid=uuid)

    if user_uuid.active == False:
        return redirect('customer:thanks')

    carts = ''
    orders = ''
    orders_in_cart = 0
    orders_in_order = 0

    categories = Category.objects.defer('created_at').order_by('id')
    table_num = request.session['table']
    same_user_table_list = nonLoginUser.objects.defer(
        'created_at').filter(table=table_num, active=True)

    # そのユーザー毎がオーダーした内容をまとめたCartリストを作成
    for same_user in same_user_table_list:
        same_user_carts = customer.models.Cart.objects.defer('created_at').filter(
            customer=same_user.uuid, curr=True).order_by('-id')
        same_user_orders = customer.models.Order.objects.defer('created_at').filter(
            customer=same_user.uuid, curr=True).order_by('-id')

        for each in same_user_carts:
            orders_in_cart += int(each.menu.price) * int(each.num)
        for each in same_user_orders:
            same_user.price = 0
            same_user.price += int(each.menu.price) * int(each.num)
            same_user.price += same_user.nomiho_price
            same_user.save()
            orders_in_order += same_user.price

        carts = list(chain(carts, same_user_carts))
        orders = list(chain(orders, same_user_orders))

    total_price = orders_in_cart + orders_in_order

    request.session['total_price'] = total_price

    ctx = {
        'categories': categories,
        'carts': carts,
        'orders': orders,
        'orders_in_cart': orders_in_cart,
        'orders_in_order': orders_in_order,
        'total_price': total_price,
        'user_uuid': user_uuid,
    }

    return render(request, 'customer/history.html', ctx)


# 伝票はテーブル1つにつき1画面で表示できればいい
def stop(request):
    try:
        request.session['nonloginuser_uuid']
    except Exception:
        messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
        return redirect('customer:table')

    try:
        total_price = request.session['total_price']
    except Exception:
        messages.info(request, f'アカウントの有効期限が切れました。')
        return redirect('customer:history')

    orders = ''

    try:
        # ユーザーのテーブル番号と同じで、かつactiveステータスのユーザーを抽出
        table_num = request.session['table']
    except Exception:
        messages.info(request, f'アカウントの有効期限が切れました。')
        return redirect('customer:history')

    same_user_table_list = nonLoginUser.objects.defer(
        'created_at').filter(table=table_num, active=True)

    for same_user in same_user_table_list:
        same_user_orders = customer.models.Order.objects.defer('created_at').filter(
            customer=same_user.uuid, curr=True).order_by('-id')

        orders = list(chain(orders, same_user_orders))

    # # オーダーストップ時に、同じテーブルにいる全てのユーザーをis_activte=Falseにする
    # for same_user in same_user_table_list:

    #     same_user.active = False
    #     same_user.save()

    ctx = {
        'total_price': total_price,
        'orders': orders,
    }

    messages.info(request, f'この画面をスクリーンショットしてお会計の際に表示してください。')

    return render(request, 'customer/stop.html', ctx)


def revert(request):
    try:
        uuid = request.session['nonloginuser_uuid']
    except Exception:
        messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
        return redirect('customer:table')

    user_uuid = nonLoginUser.objects.get(uuid=uuid)

    if user_uuid.active == False:
        user_uuid.active = True
        user_uuid.save()

        messages.info(
            request, f'あなたのアカウントのオーダーストップを取り消しました。同じテーブルの他の方も注文をする場合は、同様に先ほどのページの「オーダーストップの取消」をタップして、アカウントを復帰させてください。')

    return redirect('customer:menu')


def thanks(request):
    return render(request, 'customer/thanks.html')
