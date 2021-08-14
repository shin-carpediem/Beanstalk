from restaurant.views import order_status_ch
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Sum
from django.shortcuts import resolve_url
from itertools import chain
import time
import requests
import customer.models
from .function import permission, judging, expired
from account.models import Table, User, nonLoginUser
from restaurant.models import Allergy, Category, Menu, Nomiho
from beanstalk.settings import DEBUG, ONE_SIGNAL_REST_API_KEY


# Create your views here.
def stop_nomiho(request, duration):
    uuid = request.session['nonloginuser_uuid']
    user_uuid = nonLoginUser.objects.get(uuid=uuid)

    # TODO: sleepだと止まる
    time.sleep(int(duration)*60)
    user_uuid.nomiho = False
    user_uuid.save()


def index(request):
    return render(request, 'customer/index.html')


def table(request):
    user = request.user

    # 新規/既存をセッションで判断する
    # 新規
    if not 'nonloginuser_uuid' in request.session:

        if user.is_authenticated:
            request.session.flush()
            return redirect('restaurant:logout')
        else:
            return render(request, 'customer/table.html')
    # 既存
    else:
        return redirect('customer:menu')


def waiting_admin(request):

    expired(request)

    uuid = request.session['nonloginuser_uuid']
    user_uuid = nonLoginUser.objects.get(uuid=uuid)

    if user_uuid.allowed == 'pre_admin':
        return render(request, 'customer/waiting_admin.html')
    else:
        return redirect('customer:menu')


def waiting(request):

    expired(request)

    uuid = request.session['nonloginuser_uuid']
    user_uuid = nonLoginUser.objects.get(uuid=uuid)

    if user_uuid.allowed == 'denied':
        return redirect('customer:denied')
    elif user_uuid.allowed == 'allowed':
        messages.info(request, f'承認されました')
        return redirect('customer:menu')
    else:
        return render(request, 'customer/waiting.html')


def judge(request):
    return render(request, 'customer/judge.html')


def allowing(request):

    user = request.user
    if not user.is_authenticated:

        expired(request)

        uuid = request.session['nonloginuser_uuid']
        user_uuid = nonLoginUser.objects.get(uuid=uuid)

        if user_uuid.allowed in ['unknown', 'denied']:
            return redirect('customer:waiting')

        if user_uuid.active == False:
            request.session.flush()
            return redirect('customer:thanks')

        # unknownが一人以上いたら、その人たちをallowedにする
        table_num = request.session['table']
        unknown_user_list = nonLoginUser.objects.defer(
            'created_at').filter(allowed='unknown', table=table_num, active=True)

        if unknown_user_list.count() > 0:
            for unknown_user in unknown_user_list:
                unknown_user.allowed = 'allowed'
                unknown_user.save()

    return redirect('customer:menu')


def deny(request):

    expired(request)

    uuid = request.session['nonloginuser_uuid']
    user_uuid = nonLoginUser.objects.get(uuid=uuid)

    if user_uuid.allowed in ['unknown', 'denied']:
        return redirect('customer:waiting')

    if user_uuid.active == False:
        request.session.flush()
        return redirect('customer:thanks')

    # unknownが一人以上いたら、その人たちをdeniedにする
    table_num = request.session['table']

    unknown_user_list = nonLoginUser.objects.defer(
        'created_at').filter(allowed='unknown', table=table_num, active=True)

    if unknown_user_list.count() > 0:
        for unknown_user in unknown_user_list:
            unknown_user.allowed = 'denied'
            unknown_user.save()

    return redirect('customer:menu')


def denied(request):
    return render(request, 'customer/denied.html')


def menu(request):
    user = request.user

    categories = Category.objects.defer('created_at').order_by('id')
    allergies = Allergy.objects.defer('created_at').order_by('id')

    restaurant_name = None
    restaurant_logo = None
    user_uuid = None
    same_num = None
    nomiho_is_started = False

    # NOTE: static
    # from here
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
    # to here

    if user.is_authenticated:
        table_num = '管理者'
    else:

        # 新規の客かどうかをセッションで判断する
        # 新規
        if not 'nonloginuser_uuid' in request.session:
            table_num = request.GET.get('table')

            # 店側から承認を得る1人目のテーブルユーザー（adminユーザー）か、1人目のテーブルユーザーからの承認を得るユーザーかの分岐点
            # 現在のテーブルで最初の1人の場合
            if nonLoginUser.objects.defer('created_at').filter(table=table_num, active=True).count() == 0:
                newtable = Table(table=table_num, active=True)
                newtable.save()

                # 開発する時は不便なのでadminにしてしまう
                if DEBUG:
                    newuser = nonLoginUser(
                        allowed="admin", table=table_num, active=True)
                else:
                    newuser = nonLoginUser(
                        allowed="pre_admin", table=table_num, active=True)
                newuser.save()

                uuid = str(newuser.uuid)
                user_uuid = newuser

                # レストラン名のセッションを作成
                request.session['restaurant_name'] = restaurant_name
                # レストランのロゴのセッションを作成
                request.session['restaurant_logo'] = restaurant_logo
                # テーブル番号のセッションを作成
                request.session['table'] = table_num
                # uuidのセッションを作成
                request.session['nonloginuser_uuid'] = uuid

                return redirect('customer:waiting_admin')
            # 他に1人以上いる場合
            else:
                newuser = nonLoginUser(table=table_num, active=True)
                newuser.save()

                same_table = Table.objects.get(table=table_num, active=True)
                same_table.user += 1
                same_table.save()

                uuid = str(newuser.uuid)
                user_uuid = newuser

                # レストラン名のセッションを作成
                request.session['restaurant_name'] = restaurant_name
                # レストランのロゴのセッションを作成
                request.session['restaurant_logo'] = restaurant_logo
                # テーブル番号のセッションを作成
                request.session['table'] = table_num
                # uuidのセッションを作成
                request.session['nonloginuser_uuid'] = uuid

            if newuser.allowed == 'unknown':
                return redirect('customer:waiting')

            if newuser.allowed == 'denied':
                return redirect('customer:denied')

        # 既存
        else:

            uuid = request.session['nonloginuser_uuid']
            try:
                user_uuid = nonLoginUser.objects.get(uuid=uuid)
            except Exception:
                return redirect('customer:index')
            permission(user_uuid)
            # unknownを検知したらallow.htmlに遷移させる
            table_num = request.session['table']
            judging(table_num)

        same_user_table = nonLoginUser.objects.defer(
            'created_at').filter(table=table_num, active=True)
        same_num = same_user_table.count()

        # 後からやってきた客よりも先に飲み放題を開始していた場合、
        # 後から来た客のメニューにも飲み放題開始ボタンを表示させないようにする
        # 兼メニューを選択できるようにする
        same_user_table_list = nonLoginUser.objects.defer(
            'created_at').filter(table=table_num, active=True, nomiho=True)

        same_table_num = same_user_table_list.count()

        if same_table_num != 0:
            user_uuid.nomiho = True
            user_uuid.save()

            nomiho_is_started = True

    if 'category_name' in request.session:
        category = request.session['category_name']
    # カテゴリーセッションがない場合（つまり一番最初に訪れた時）は、一番最初のカテゴリーのページとする
    else:

        try:
            category = categories[0].id
        except Exception:
            category = None

        # カテゴリーIDのセッションを作成
        request.session['category_name'] = category

    if category != None:
        menus = Menu.objects.defer('chef_img', 'comment', 'created_at').filter(
            category=category).order_by('-id')
    else:
        menus = Menu.objects.defer(
            'chef_img', 'comment', 'created_at').order_by('-id')

    ctx = {
        'categories': categories,
        'menus': menus,
        'allergies': allergies,
        'user_uuid': user_uuid,
        'same_num': same_num,
        'nomiho_is_started': nomiho_is_started,
    }

    return render(request, 'customer/menu.html', ctx)


def filter(request, category_id):
    user = request.user
    same_num = None
    nomiho_is_started = False

    if not user.is_authenticated:
        expired(request)

    try:
        category_id = Category.objects.get(id=category_id)

        # カテゴリーのセッションを更新
        request.session['category_name'] = category_id.id
        menus = Menu.objects.defer('chef_img', 'comment', 'created_at').filter(
            category=category_id).order_by('-id')
    except Exception:
        menus = None

    try:

        uuid = request.session['nonloginuser_uuid']
        try:
            user_uuid = nonLoginUser.objects.get(uuid=uuid)
        except Exception:
            return redirect('customer:index')
        permission(user_uuid)
        table_num = request.session['table']
        judging(table_num)

        # 後からやってきた客よりも先に飲み放題を開始していた場合、
        # 後から来た客のメニューにも飲み放題開始ボタンを表示させないようにする
        # 兼メニューを選択できるようにする
        same_user_table = nonLoginUser.objects.defer(
            'created_at').filter(table=table_num, active=True)
        same_num = same_user_table.count()

        same_user_table_list = nonLoginUser.objects.defer(
            'created_at').filter(table=table_num, active=True, nomiho=True)

        same_table_num = same_user_table_list.count()

        if same_table_num != 0:
            user_uuid.nomiho = True
            user_uuid.save()

            nomiho_is_started = True

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
        'same_num': same_num,
        'nomiho_is_started': nomiho_is_started,
    }

    # 飲み放題のカテゴリーを選択した場合
    if category_id.nomiho == True:
        nomihos = Nomiho.objects.defer('created_at').order_by('-id')
        ctx['nomihos'] = nomihos
        ctx['nomiho_category'] = "Yes"

        if user_uuid != None:

            if user_uuid.nomiho == False:
                messages.info(request, f'このページのメニューは飲み放題を開始すると注文できます')
    else:
        ctx['nomiho_category'] = "No"

    return render(request, 'customer/menu.html', ctx)


def menu_detail(request, menu_id):
    user = request.user

    if not user.is_authenticated:

        expired(request)
        uuid = request.session['nonloginuser_uuid']
        user_uuid = nonLoginUser.objects.get(uuid=uuid)
        permission(user_uuid)
        table_num = request.session['table']
        judging(table_num)

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
def request(request, menu_id):
    menu_request = request.POST.get('request')
    request.session['menu_request'] = {menu_id: menu_request}
    return redirect('customer:menu_detail', menu_id=menu_id)


@require_POST
def cart(request):
    expired(request)
    uuid = request.session['nonloginuser_uuid']
    user_uuid = nonLoginUser.objects.get(uuid=uuid)
    permission(user_uuid)
    table_num = request.session['table']
    judging(table_num)

    user_table = user_uuid.table
    same_table_user_list = nonLoginUser.objects.defer(
        'created_at').filter(table=user_table, active=True)
    same_table_cart_list = ''

    for same_table_user in same_table_user_list:
        same_table_cart = customer.models.Cart.objects.defer(
            'created_at').filter(customer=same_table_user, curr=True).order_by('-id')
        same_table_cart_list = list(
            chain(same_table_cart_list, same_table_cart))

    # Cartデータの保存
    menu_id = request.POST.get('menu_id')
    cart_num = request.POST.get('cart_num')
    menu_instance = Menu.objects.get(id=menu_id)
    if request.session['menu_request'] != None:
        menu_request = request.session['menu_request'][menu_id]
    else:
        menu_request = None

    # すでにカートに同じ商品が追加されていないかチェック
    try:
        cart = customer.models.Cart.objects.get(menu=menu_instance, curr=True)
        cart.num += int(cart_num)
        if not menu_request == None:
            cart.request = menu_request
    except Exception:
        if not menu_request == None:
            cart = customer.models.Cart(menu=menu_instance, num=cart_num, request=menu_request,
                                        customer=user_uuid, curr=True)
        else:
            cart = customer.models.Cart(menu=menu_instance, num=cart_num,
                                        customer=user_uuid, curr=True)

    cart.save()
    request.session['menu_request'] = None

    return redirect('customer:menu')


def cart_static(request):
    expired(request)
    uuid = request.session['nonloginuser_uuid']
    user_uuid = nonLoginUser.objects.get(uuid=uuid)
    permission(user_uuid)
    table_num = request.session['table']
    judging(table_num)

    carts = ''
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
    expired(request)
    uuid = request.session['nonloginuser_uuid']
    user_uuid = nonLoginUser.objects.get(uuid=uuid)
    permission(user_uuid)
    table_num = request.session['table']
    judging(table_num)

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
    expired(request)
    uuid = request.session['nonloginuser_uuid']
    user_uuid = nonLoginUser.objects.get(uuid=uuid)
    permission(user_uuid)
    table_num = request.session['table']
    judging(table_num)

    cart_id = request.GET.get('cart_id')
    type = request.GET.get('type')

    # Cartデータの更新
    try:
        cart = customer.models.Cart.objects.get(id=cart_id)

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
    expired(request)
    uuid = request.session['nonloginuser_uuid']
    user_uuid = nonLoginUser.objects.get(uuid=uuid)
    permission(user_uuid)
    table_num = request.session['table']
    judging(table_num)

    try:
        # ユーザーのテーブル番号と同じで、かつactiveステータスのユーザーを抽出
        same_user_table_list = nonLoginUser.objects.defer(
            'created_at').filter(table=table_num, active=True)

        # そのユーザー毎がカートに追加した内容をまとめたCartリストを作成
        for same_user in same_user_table_list:
            same_user_carts = customer.models.Cart.objects.defer('created_at').filter(
                customer=same_user.uuid, curr=True).order_by('-id')

            # 同時に同じテーブルの人が注文した際は後者を弾く為
            if not same_user_carts == None:

                # テーブル毎の合計金額をオーダー時に加算する
                table_query = Table.objects.get(table=table_num, active=True)

                # ひとつひとつ、オブジェクトをカートからオーダーに移行
                for each in same_user_carts:
                    order = customer.models.Order(status='調理中', menu=each.menu,
                                                  num=each.num, customer=each.customer, curr=True)
                    order.save()
                    price = (order.menu.price * order.num)
                    same_user.price += int(price)
                    table_query.price += int(price)

                same_user.save()
                table_query.save()
                # MEMO: be careful not to switch save and delete
                same_user_carts.delete()
            else:
                messages.info(request, f"注文を先ほど承っております。")
                return redirect('customer:cart')

        # オーダーをブラウザ通知
        try:
            data = {
                'app_id': 'cebff79b-a399-438a-81fb-fa4c72364762',
                'included_segments': ['All'],
                'contents': {'ja': str(table_num) + '番テーブル'},
                'headings': {'ja': '注文がきました'},
                'url': resolve_url('restaurant:order_manage'),
            }
            requests.post(
                "https://onesignal.com/api/v1/notifications",
                headers={
                    'Authorization': ONE_SIGNAL_REST_API_KEY},
                json=data,
            )
            print(data)
        except Exception:
            print("false..")

    except Exception:
        pass

    messages.info(request, f"注文を承りました。今しばらくお待ちください")

    return redirect('customer:menu')


# 飲み放題開始用のボタン
@require_GET
def nomiho(request, nomiho_id):
    user = request.user
    if user.is_authenticated:
        request.session.flush()
        return redirect('customer:index')
    else:

        expired(request)
        uuid = request.session['nonloginuser_uuid']
        user_uuid = nonLoginUser.objects.get(uuid=uuid)
        permission(user_uuid)
        table_num = request.session['table']
        judging(table_num)

        # 同じテーブルのそれぞれのお客さんの合計金額に加算する。また、飲み放題に関する情報を記述する。
        try:
            nomiho_query = Nomiho.objects.get(id=nomiho_id)

            same_user_table_list = nonLoginUser.objects.defer(
                'created_at').filter(table=table_num, nomiho=False, active=True)

            nomiho_num = request.GET.get('nomiho_num')

            # 飲み放題の内容を店側に伝えるデータを作成
            nomiho_order = customer.models.NomihoOrder(status='開始中', nomiho=nomiho_query, table=table_num,
                                                       num=nomiho_num, customer=user_uuid, curr=True)
            nomiho_order.save()

            table_query = Table.objects.get(table=table_num, active=True)

            for same_user in same_user_table_list:
                same_user.price += int(nomiho_query.price)
                # 各々の「飲み放題」ステータス：yes/noをyesにする
                same_user.nomiho = True
                same_user.nomiho_name = nomiho_query.name
                same_user.nomiho_price += int(nomiho_query.price)
                # 合計金額に飲み放題の金額を足す
                same_user.price += same_user.nomiho_price
                same_user.save()

                table_query.price += int(nomiho_query.price)
                table_query.save()

                # TODO:
                duration = nomiho_query.duration
                # stop_nomiho(request, duration)

            messages.info(
                request, f'🍺 飲み放題を開始しました！！🍶  制限時間は{duration}分です！')

        except Exception:
            pass

        return redirect('customer:menu')


def history(request):
    expired(request)
    uuid = request.session['nonloginuser_uuid']
    user_uuid = nonLoginUser.objects.get(uuid=uuid)
    permission(user_uuid)
    table_num = request.session['table']
    judging(table_num)

    carts = ''
    orders = ''
    orders_in_cart = 0

    categories = Category.objects.defer('created_at').order_by('id')
    same_user_table_list = nonLoginUser.objects.defer(
        'created_at').filter(table=table_num, active=True)

    try:
        table_query = Table.objects.get(table=table_num, active=True)
    except Exception:
        messages.info(request, f"申し訳ありません。エラーが発生しました。")
        return redirect('customer:menu')

    orders_in_order = table_query.price

    # そのユーザー毎がオーダーした内容をまとめたCartリストを作成
    for same_user in same_user_table_list:
        same_user_carts = customer.models.Cart.objects.defer('created_at').filter(
            customer=same_user.uuid, curr=True).order_by('-id')
        same_user_orders = customer.models.Order.objects.defer('created_at').exclude(status='キャンセル').filter(
            customer=same_user.uuid, curr=True).order_by('-id')

        for each in same_user_carts:
            orders_in_cart += int(each.menu.price) * int(each.num)
        for each in same_user_orders:
            same_user.price = 0
            same_user.price += int(each.menu.price) * int(each.num)
            same_user.save()

        carts = list(chain(carts, same_user_carts))
        orders = list(chain(orders, same_user_orders))

    total_price = int(orders_in_cart) + int(orders_in_order)

    request.session['orders_in_cart'] = str(orders_in_cart)
    request.session['total_price'] = str(total_price)

    ctx = {
        'categories': categories,
        'carts': carts,
        'orders': orders,
        'orders_in_order': orders_in_order,
        'user_uuid': user_uuid,
    }

    return render(request, 'customer/history.html', ctx)


# 伝票はテーブル1つにつき1画面で表示できればいい
def stop(request):

    expired(request)
    uuid = request.session['nonloginuser_uuid']
    user_uuid = nonLoginUser.objects.get(uuid=uuid)
    permission(user_uuid)
    table_num = request.session['table']
    judging(table_num)

    orders = ''

    table = Table.objects.get(table=int(table_num), active=True)

    same_user_table_list = nonLoginUser.objects.defer(
        'created_at').filter(table=table_num, active=True)

    nomiho_orders = customer.models.NomihoOrder.objects.filter(
        table=table_num, curr=True)

    for same_user in same_user_table_list:
        same_user_orders = customer.models.Order.objects.defer('created_at').exclude(status='キャンセル').filter(
            customer=same_user.uuid, curr=True).order_by('-id')

        orders = list(chain(orders, same_user_orders))

    ctx = {
        'table': table,
        'nomiho_orders': nomiho_orders,
        'orders': orders,
    }

    messages.info(request, f'この画面をスクリーンショットしてお会計の際に表示してください。')

    return render(request, 'customer/stop.html', ctx)


def thanks(request):
    return render(request, 'customer/thanks.html')
