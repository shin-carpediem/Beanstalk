from django.contrib import messages
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db.models import Q, Sum
from itertools import chain
from account.models import User, nonLoginUser
from restaurant.models import Allergy, Category, Menu, Nomiho


# Create your views here.
def index(request):
    return render(request, 'customer/index.html')


def table(request):
    user = request.user

    # 新規/既存をセッションで判断する
    # 新規
    if not request.session.session_key:

        restaurant_name = None
        try:
            restaurant = User.objects.get(id=1)
            restaurant_name = restaurant.name
        except Exception:
            pass
        try:
            restaurant = User.objects.get(id=2)
            restaurant_name = restaurant.name
        except Exception:
            pass
        try:
            restaurant = User.objects.get(id=3)  # MEMO: be careful of id, client id should be 3.
            restaurant_name = restaurant.name
        except Exception:
            pass

        if user.is_authenticated:
            return redirect('restaurant:logout')
        else:
            None

            ctx = {
                'restaurant_name': restaurant_name,
            }

            return render(request, 'customer/table.html', ctx)
    # 既存
    else:
        return redirect('customer:menu')


def menu(request):
    user = request.user

    categories = Category.objects.defer('created_at').order_by('id')
    try:
        first_category = categories[0]
        menus = Menu.objects.defer('created_at').filter(
            category=first_category).order_by('-id')
        category_name = first_category.name
    except Exception:
        pass
    allergies = Allergy.objects.all().order_by('id')

    restaurant_name = None
    try:
        restaurant = User.objects.get(id=1)
        restaurant_name = restaurant.name
    except Exception:
        pass
    try:
        restaurant = User.objects.get(id=2)
        restaurant_name = restaurant.name
    except Exception:
        pass
    try:
        restaurant = User.objects.get(id=3)
        restaurant_name = restaurant.name
    except Exception:
        pass

    if user.is_authenticated:
        table_num = '管理者'
    else:

        try:
            table_num = request.POST.get('table')
        except Exception:
                messages.info(request, f'注文を続けるにはテーブル番号を入力してください。')
                return redirect('customer:table')

        # 新規の客かどうかをセッションで判断する
        # 新規
        if not request.session.session_key:

            try:
                newuser = nonLoginUser(table=table_num,)

            except Exception:
                messages.info(request, f'申し訳ございません。エラーが発生しました。')
                return redirect('customer:index')

            newuser.active = True
            newuser.save()
            uuid = str(newuser.uuid)

            # セッション開始
            request.session.create()
            # テーブル番号のセッションを作成
            request.session['table'] = table_num
            # uuidのセッションを作成
            request.session['nonloginuser_uuid'] = uuid

    ctx = {
        'restaurant_name': restaurant_name,
        'categories': categories,
        'category_name': category_name,
        'menus': menus,
        'allergies': allergies,
    }

    return render(request, 'customer/menu.html', ctx)


def filter(request):
    user = request.user
    # 店側から
    if user.is_authenticated:
        table_num = "管理者"
    # 客側から
    else:

        # テーブル番号を基に既存の客の情報を引き出す為の準備
        try:
            table_num = request.session['table']
        except Exception:
                messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
                return redirect('customer:table')

    try:
        category_name = request.POST.get('category')
        category_id = Category.objects.get(name=category_name)
        menus = Menu.objects.defer('created_at').filter(
            category=category_id).order_by('-id')
    except Exception:
        menus = None

    try:
        uuid = request.session['nonloginuser_uuid']
        user_uuid = nonLoginUser.objects.get(uuid=uuid)
    # まだ1人もお客さんが使用していない初期設定時を想定
    except Exception:
        user_uuid = None

    categories = Category.objects.defer('created_at').order_by('id')
    allergies = Allergy.objects.defer('created_at').order_by('id')

    restaurant_name = None
    try:
        restaurant = User.objects.get(id=1)
        restaurant_name = restaurant.name
    except Exception:
        pass
    try:
        restaurant = User.objects.get(id=2)
        restaurant_name = restaurant.name
    except Exception:
        pass
    try:
        restaurant = User.objects.get(id=3)
        restaurant_name = restaurant.name
    except Exception:
        pass

    ctx = {
        'restaurant_name': restaurant_name,
        'category_name': category_name,
        'categories': categories,
        'menus': menus,
        'allergies': allergies,
        'user_uuid': user_uuid,
    }

    # 飲み放題を選択した場合
    nomihos = Nomiho.objects.defer('created_at').order_by('-id')
    ctx['nomihos'] = nomihos

    messages.info(request, f'このページは飲み放題用です')

    return render(request, 'customer/menu.html', ctx)


def menu_detail(request, menu_id):
    user = request.user
    if user.is_authenticated:
        table_num = "管理者"
    else:
        # テーブル番号を基に既存の客の情報を引き出す為の準備
        try:
            table_num = request.session['table']
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
    # テーブル番号を基に既存の客の情報を引き出す為の準備
    try:
        table_num = request.session['table']
    except Exception:
            messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
            return redirect('customer:table')

    from .models import Cart

    # メニュー詳細(/detail/)から見るルート
    if request.POST.get('direct') == 'direct':

        restaurant_name = None
        try:
            restaurant = User.objects.get(id=1)
            restaurant_name = restaurant.name
        except Exception:
            pass
        try:
            restaurant = User.objects.get(id=2)
            restaurant_name = restaurant.name
        except Exception:
            pass
        try:
            restaurant = User.objects.get(id=3)
            restaurant_name = restaurant.name
        except Exception:
            pass

        # Cartデータの保存
        menu_id = request.POST.get('menu_id')
        cart_num = request.POST.get('cart_num')
        menu_instance = Menu.objects.get(id=menu_id)
        uuid = request.session['nonloginuser_uuid']
        user_uuid = nonLoginUser.objects.get(uuid=uuid)

        try:
            cart = Cart(menu=menu_instance, num=cart_num, customer=user_uuid)
            cart.save()
        except:
            pass

        categories = Category.objects.defer('created_at').order_by('id')
        try:
            first_category = categories[0]
            category_name = first_category.name
            menus = Menu.objects.filter(
                category=first_category).order_by('-id')
        except Exception:
            category_name = None
            menus = None
        allergies = Allergy.objects.defer('created_at').order_by('id')

        ctx = {
            'restaurant_name': restaurant_name,
            'categories': categories,
            'category_name': category_name,
            'menus': menus,
            'allergies': allergies,
        }

        return render(request, 'customer/menu.html', ctx)
    # メニューIDの情報を保持していない、一覧ページからのルート
    else:
        carts = ''
        # ユーザーのテーブル番号と同じで、かつactiveステータスのユーザーを抽出
        same_user_table_list = nonLoginUser.objects.defer(
            'created_at').filter(table=table_num, active=True)

        # そのユーザー毎がオーダーした内容をまとめたCartリストを作成
        for same_user in same_user_table_list:
            same_user_carts = Cart.objects.defer('created_at').filter(
                customer=same_user.uuid).order_by('-id')

            carts = list(chain(same_user_carts))
            # TODO:
            # 同じ商品は個数をまとめたい

        ctx = {
            'carts': carts,
        }

        return render(request, 'customer/cart.html', ctx)


def cart_detail(request, menu_id):
    # テーブル番号を基に既存の客の情報を引き出す為の準備
    try:
        table_num = request.session['table']
    except Exception:
            messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
            return redirect('customer:table')

    curr_num = request.POST.get('curr_num')
    cart_id = request.POST.get('cart_id')
    menu = get_object_or_404(Menu, pk=menu_id)

    allergies = Allergy.objects.defer('created_at').order_by('id')
    has_allergies = menu.allergies.defer('created_at').order_by('id')

    # TODO: 同じ商品を1つにまとめる際に使えるので、残しておく。
    # from .models import Cart
    # curr_num = 0

    # same_user_table_list = nonLoginUser.objects.defer(
    #     'created_at').filter(table=table_num, active=True)

    # # 同じテーブルでカートに追加された、同一の商品の全ての個数を表示
    # for same_user in same_user_table_list:
    #     same_user_carts = Cart.objects.defer('created_at').filter(menu=menu,
    #                                                               customer=same_user.uuid).order_by('-id')

    #     for each in same_user_carts:
    #         curr_num += int(each.num)

    ctx = {
        'menu': menu,
        'allergies': allergies,
        'has_allergies': has_allergies,
        'curr_num': curr_num,
        'cart_id': cart_id,
    }

    return render(request, 'customer/cart_detail.html', ctx)


@require_POST
def cart_ch(request):
    # テーブル番号を基に既存の客の情報を引き出す為の準備
    try:
        table_num = request.session['table']
    except Exception:
            messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
            return redirect('customer:table')

    cart_id = request.POST.get('cart_id')
    type = request.POST.get('type')

    restaurant_name = None
    try:
        restaurant = User.objects.get(id=1)
        restaurant_name = restaurant.name
    except Exception:
        pass
    try:
        restaurant = User.objects.get(id=2)
        restaurant_name = restaurant.name
    except Exception:
        pass
    try:
        restaurant = User.objects.get(id=3)
        restaurant_name = restaurant.name
    except Exception:
        pass

    from .models import Cart

    # Cartデータの更新
    try:
        cart = Cart.objects.defer('created_at').get(id=cart_id)

        if type == 'change':
            cart_num = request.POST.get('cart_num')
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
        same_user_carts = Cart.objects.defer('created_at').filter(
            customer=same_user.uuid).order_by('-id')

        carts = list(chain(same_user_carts))

    ctx = {
        'restaurant_name': restaurant_name,
        'carts': carts,
    }

    return render(request, 'customer/cart.html', ctx)


@require_POST
def order(request):
    # テーブル番号を基に既存の客の情報を引き出す為の準備
    try:
        table_num = request.session['table']
    except Exception:
            messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
            return redirect('customer:table')

    categories = Category.objects.defer('created_at').order_by('id')
    try:
        first_category = categories[0]
        menus = Menu.objects.defer('created_at').filter(
            category=first_category).order_by('-id')
        category_name = first_category.name
    except Exception:
        pass

    restaurant_name = None
    try:
        restaurant = User.objects.get(id=1)
        restaurant_name = restaurant.name
    except Exception:
        pass
    try:
        restaurant = User.objects.get(id=2)
        restaurant_name = restaurant.name
    except Exception:
        pass
    try:
        restaurant = User.objects.get(id=3)
        restaurant_name = restaurant.name
    except Exception:
        pass

    try:
        from .models import Cart, Order
        # ユーザーのテーブル番号と同じで、かつactiveステータスのユーザーを抽出
        same_user_table_list = nonLoginUser.objects.defer(
            'created_at').filter(table=table_num, active=True)

        # そのユーザー毎がオーダーした内容をまとめたCartリストを作成
        for same_user in same_user_table_list:
            same_user_carts = Cart.objects.defer('created_at').filter(
                customer=same_user.uuid).order_by('-id')

            cart_price = 0

            for each in same_user_carts:
                order = Order(status='調理中', menu=each.menu,
                                num=each.num, customer=each.customer)
                order.save()
                cart_price = cart_price + (each.menu.price * each.num)

            same_user.price += int(cart_price)

            same_user_carts.delete()

        # push notification
        # from django.contrib.auth.models import User
        # user = User.objects.get(id=1)
        from webpush import send_user_notification
        payload = {"head": "新しい注文がきました", "body": "{table_num}番テーブルからの注文です"}
        send_user_notification(user=restaurant, payload=payload, ttl=1000)
    except Exception:
        pass

    ctx = {
        'restaurant_name': restaurant_name,
        'categories': categories,
        'category_name': category_name,
        'menus': menus,
    }
    messages.info(request, f"注文を承りました。今しばらくお待ちください")

    return render(request, 'customer/menu.html', ctx)


# 飲み放題開始用のボタン
@require_POST
def nomiho(request):
    # テーブル番号を基に既存の客の情報を引き出す為の準備
    try:
        table_num = request.session['table']
    except Exception:
            messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
            return redirect('customer:table')

    nomiho_type = request.POST.get('nomiho_type')

    category_id = Category.objects.defer('created_at').filter(nomiho='True')[0]
    category_name = category_id.name
    categories = Category.objects.defer('created_at').order_by('id')
    menus = Menu.objects.defer('created_at').filter(
        category=category_id).order_by('-id')
    allergies = Allergy.objects.defer('created_at').order_by('id')
    nomiho_query = Nomiho.objects.get(id=nomiho_type)

    restaurant_name = None
    try:
        restaurant = User.objects.get(id=1)
        restaurant_name = restaurant.name
    except Exception:
        pass
    try:
        restaurant = User.objects.get(id=2)
        restaurant_name = restaurant.name
    except Exception:
        pass
    try:
        restaurant = User.objects.get(id=3)
        restaurant_name = restaurant.name
    except Exception:
        pass

    # 同じテーブルのそれぞれのお客さんの合計金額に加算する。また、飲み放題に関する情報を記述する。
    if nomiho_query != None:
        same_user_table_list = nonLoginUser.objects.defer(
            'created_at').filter(table=table_num, active=True)

        for same_user in same_user_table_list:
            same_user.price = int(same_user.price) + \
                int(nomiho_query.price)
            same_user.nomiho = True
            same_user.nomiho_name = nomiho_query.name
            same_user.nomiho_price += int(nomiho_query.price)
            same_user.save()

    time = nomiho_query.duration

    messages.info(request, f'🍺 飲み放題が開始されました！！🍶  制限時間は{time}分です！')

    ctx = {
        'restaurant_name': restaurant_name,
        'category_name': category_name,
        'categories': categories,
        'menus': menus,
        'allergies': allergies,
        'nomiho_query': nomiho_query,
    }

    return render(request, 'customer/menu.html', ctx)


def history(request):
    # テーブル番号を基に既存の客の情報を引き出す為の準備
    try:
        table_num = request.session['table']
    except Exception:
            messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
            return redirect('customer:table')

    uuid = request.session['nonloginuser_uuid']
    user_uuid = nonLoginUser.objects.get(uuid=uuid)

    from .models import Cart, Order
    carts = ''
    orders = ''
    orders_in_cart = 0
    orders_in_order = 0

    same_user_table_list = nonLoginUser.objects.defer(
        'created_at').filter(table=table_num, active=True)

    # そのユーザー毎がオーダーした内容をまとめたCartリストを作成
    for same_user in same_user_table_list:
        same_user_carts = Cart.objects.defer('created_at').filter(
            customer=same_user.uuid).order_by('-id')
        same_user_orders = Order.objects.defer('created_at').filter(
            customer=same_user.uuid).order_by('-id')

        carts = list(chain(same_user_carts))
        orders = list(chain(same_user_orders))

        for each in same_user_carts:
            orders_in_cart += int(each.menu.price) * int(each.num)
        for each in same_user_orders:
            same_user.price += int(each.menu.price) * int(each.num)

        same_user.price += same_user.nomiho_price
        orders_in_order += same_user.price

    total_price = orders_in_cart + orders_in_order

    ctx = {
        'table_num': table_num,
        'carts': carts,
        'orders': orders,
        'orders_in_cart': orders_in_cart,
        'orders_in_order': orders_in_order,
        'user_uuid': user_uuid,
        'total_price': total_price,
    }

    return render(request, 'customer/history.html', ctx)


# TODO:
def stop(request):
    # テーブル番号を基に既存の客の情報を引き出す為の準備
    try:
        table_num = request.session['table']
    except Exception:
            messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
            return redirect('customer:table')

    total_price = request.POST.get('total_price')

    try:
        # ユーザーのテーブル番号と同じで、かつactiveステータスのユーザーを抽出
        same_user_table_list = nonLoginUser.objects.defer(
            'created_at').filter(table=table_num, active=True)

        from .models import Order
        orders = ''
        for same_user in same_user_table_list:
            same_user_orders = Order.objects.defer('created_at').filter(
                customer=same_user.uuid).order_by('-id')

            orders = list(chain(same_user_orders))

        # TODO:
        # やっぱりオーダーストップを元に戻したい客用に、False→Trueにすべきユーザーリストを保存しておく
        user_uuid_list = ''

        # オーダーストップ時に、同じテーブルにいる全てのユーザーをis_activte=Falseにする
        try:
            for same_user in same_user_table_list:

                same_user.active = False
                same_user.save()
                # ここまでは正常

                user_uuid_list = list(chain(same_user))
                print(user_uuid_list)
        except Exception:
            messages.info(request, f'申し訳ありませんがエラーが発生しました。')
            return redirect('customer:history')

    except Exception:
        messages.info(request, f'申し訳ありませんがエラーが発生しました。')
        return redirect('customer:history')

    ctx = {
        'user_uuid_list': user_uuid_list,
        'total_price': total_price,
        'orders': orders,
    }

    messages.info(request, f'リロードせずにこのままこの画面を、お会計時にお店に見せてください')

    return render(request, 'customer/stop.html', ctx)


#TODO:
@require_POST
def revert(request):
    # テーブル番号を基に既存の客の情報を引き出す為の準備
    try:
        table_num = request.session['table']
    except Exception:
            messages.info(request, f'アカウントの有効期限が切れました。新規登録してください。')
            return redirect('customer:table')

    # TODO:
    user_uuid_list = request.POST.get('user_uuid_list')
    print(user_uuid_list)
    user_list = ''

    for each in user_uuid_list:
        each_user = nonLoginUser.objects.defer('created_at').filter(uuid=each)
        user_list = list(chain(each_user))
        # user_list.append(each_user)
        print(user_list)
    print(user_list)

    try:
        # TODO:
        # オーダーストップ時に、同じテーブルにいる全てのユーザーをis_activte=Falseにする
        if user_list != []:
            for same_user in user_list:
                same_user.active = True
                same_user.save()

    except Exception:
        messages.info(request, f'申し訳ありませんがエラーが発生しました。')
        return redirect('customer:stop')

    ctx = {
    }

    return render(request, 'customer/history.html', ctx)
