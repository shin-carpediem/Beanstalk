from django.contrib import messages
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db.models import Q, Sum
import random
import string
from account.models import User, nonLoginUser
from restaurant.models import Allergy, Category, Menu
from .forms import ChooseTableForm


# Create your views here.
def non_login_user_random_code(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def index(request):
    return render(request, 'customer/index.html')


def table(request):
    try:
        restaurant = User.objects.get(id=3)
    except:
        restaurant = User.objects.get(id=1)
    restaurant_name = restaurant.name

    user = request.user
    if user.is_authenticated:
        return redirect('restaurant:logout')
    else:
        choose_table_form = ChooseTableForm(request.POST or None)

        ctx = {
            'choose_table_form': choose_table_form,
            'restaurant_name': restaurant_name,
        }

        return render(request, 'customer/table.html', ctx)


def menu(request):
    user = request.user

    categories = Category.objects.all().order_by('id')
    first_category = Category(id=1)
    menus = Menu.objects.filter(category=first_category).order_by('-id')
    allergies = Allergy.objects.all().order_by('id')
    try:
        restaurant = User.objects.get(id=3)
    except:
        restaurant = User.objects.get(id=1)
    restaurant_name = restaurant.name

    if user.is_authenticated:
        userid = '管理者'
    else:
        random_code = non_login_user_random_code(50)

        # 新規の客かどうかをセッションで判断する
        if not 'nonloginuser_uuid' in request.session:
            table_num = request.POST.get('table')
            newuser = nonLoginUser(table=table_num,)
            newuser.save()

            uuid = str(newuser.uuid)
            userid = newuser.table

            # テーブル番号と客のuuidのセットになったセッションを作成
            request.session['nonloginuser_uuid'] = {userid: uuid}

            # テーブル番号のセッションを作成
            request.session['table'] = {userid: table_num}

            # テーブル番号と客のランダムコード(ワンタイムパスワード)のセットになったセッションを作成
            request.session['nonloginuser'] = {userid: random_code}
        else:
            table_num = request.session['table'][userid]

    if user.is_authenticated:
        ctx = {
            'restaurant_name': restaurant_name,
            'table_num': table_num,
            'categories': categories,
            'menus': menus,
            'allergies': allergies,
        }
    else:
        ctx = {
            'random_code': random_code,
            'restaurant_name': restaurant_name,
            'table_num': table_num,
            'categories': categories,
            'menus': menus,
            'allergies': allergies,
        }

    return render(request, 'customer/menu.html', ctx)


@require_POST
def filter(request):
    user = request.user
    random_code = request.POST.get('random_code')
    table_num = request.POST.get('table')
    category_name = request.POST.get('category')

    category_id = Category.objects.get(name=category_name)
    categories = Category.objects.all().order_by('id')
    menus = Menu.objects.filter(category=category_id).order_by('-id')
    allergies = Allergy.objects.all().order_by('id')
    try:
        restaurant = User.objects.get(id=3)
    except:
        restaurant = User.objects.get(id=1)
    restaurant_name = restaurant.name

    # 店側から
    if user.is_authenticated:
        table_num = "管理者"
    # 客側から
    else:

        try:
            # hiddenで取得したランダムコードがセッションに保存されたものと一致しているかチェック
            if random_code == request.session['nonloginuser'][table_num]:

                random_code = non_login_user_random_code(50)
                # セッションに保存されているランダムコードの更新
                request.session['nonloginuser'] = {table_num: random_code}
        except:
            messages.info(request, f'申し訳ありません。異常なエラーが発生しました。')
            return redirect('customer:index')

    ctx = {
        'random_code': random_code,
        'restaurant_name': restaurant_name,
        'table_num': table_num,
        'category_name': category_name,
        'categories': categories,
        'menus': menus,
        'allergies': allergies,
    }

    return render(request, 'customer/menu.html', ctx)


def menu_detail(request, menu_id):
    user = request.user
    random_code = request.POST.get('random_code')
    table_num = request.POST.get('table')
    menu = get_object_or_404(Menu, pk=menu_id)

    allergies = Allergy.objects.all().order_by('id')
    has_allergies = menu.allergies.all().order_by('id')

    if user.is_authenticated:
        table_num = "管理者"
    else:

        try:
            # hiddenで取得したランダムコードがセッションに保存されたものと一致しているかチェック
            if random_code == request.session['nonloginuser'][table_num]:
                random_code = non_login_user_random_code(50)
                # セッションに保存されているランダムコードの更新
                request.session['nonloginuser'] = {table_num: random_code}
        except:
            messages.info(request, f'異常なエラーが発生しました。')
            return redirect('customer:table')

    ctx = {
        'random_code': random_code,
        'menu': menu,
        'table_num': table_num,
        'allergies': allergies,
        'has_allergies': has_allergies,
        'add_cart': "direct",
    }

    return render(request, 'customer/detail.html', ctx)


@require_POST
def cart(request):
    user = request.user
    random_code = request.POST.get('random_code')
    table_num = request.POST.get('table')
    uuid = request.session['nonloginuser_uuid'][table_num]

    if user.is_authenticated:
        table_num = "管理者"

    else:
        try:

            # hiddenで取得したランダムコードがセッションに保存されたものと一致しているかチェック
            if random_code == request.session['nonloginuser'][table_num]:
                random_code = non_login_user_random_code(50)
                # セッションに保存されているランダムコードの更新
                request.session['nonloginuser'] = {table_num: random_code}
            else:
                None
        except:
            messages.info(request, f'異常なエラーが発生しました。')
            return redirect('customer:table')

    from .models import Cart

    # メニューの詳細から見るルート
    try:
        menu_id = request.POST.get('menu_id')

        menu_instance = Menu.objects.get(id=menu_id)
        cart_num = request.POST.get('cart_num')
        user_uuid = nonLoginUser.objects.get(uuid=uuid)

        cart = Cart(menu=menu_instance, num=cart_num, customer=user_uuid)
        cart.save()
    # メニュー画面から見るルート
    except:
        None

    if request.POST.get('direct') == 'direct':
        try:
            restaurant = User.objects.get(id=3)
        except:
            restaurant = User.objects.get(id=1)
        restaurant_name = restaurant.name

        categories = Category.objects.all().order_by('id')
        first_category = Category(id=1)
        menus = Menu.objects.filter(category=first_category).order_by('-id')
        allergies = Allergy.objects.all().order_by('id')

        ctx = {
            'random_code': random_code,
            'restaurant_name': restaurant_name,
            'table_num': table_num,
            'categories': categories,
            'menus': menus,
            'allergies': allergies,
        }

        return render(request, 'customer/menu.html', ctx)
    else:
        carts = Cart.objects.filter(customer=uuid).order_by('-id')

        ctx = {
            'random_code': random_code,
            'table_num': table_num,
            'carts': carts,
        }

        return render(request, 'customer/cart.html', ctx)


@require_POST
def cart_detail(request, menu_id):
    user = request.user
    random_code = request.POST.get('random_code')
    table_num = request.POST.get('table')
    menu = get_object_or_404(Menu, pk=menu_id)

    allergies = Allergy.objects.all().order_by('id')
    has_allergies = menu.allergies.all().order_by('id')

    if user.is_authenticated:
        return redirect('restaurant:logout')
    else:

        try:
            # hiddenで取得したランダムコードがセッションに保存されたものと一致しているかチェック
            if random_code == request.session['nonloginuser'][table_num]:

                random_code = non_login_user_random_code(50)
                # セッションに保存されているランダムコードの更新
                request.session['nonloginuser'] = {table_num: random_code}
        except:
            messages.info(request, f'異常なエラーが発生しました。')
            return redirect('customer:table')

        ctx = {
            'randcom_code': random_code,
            'table_num': table_num,
            'menu': menu,
            'allergies': allergies,
            'has_allergies': has_allergies,
        }

        return render(request, 'customer/detail.html', ctx)


@require_POST
def order(request):
    user = request.user
    random_code = request.POST.get('random_code')
    table_num = request.POST.get('table')
    uuid = request.session['nonloginuser_uuid'][table_num]

    categories = Category.objects.all().order_by('id')
    first_category = Category(id=1)
    menus = Menu.objects.filter(category=first_category).order_by('-id')

    if user.is_authenticated:
        return redirect('restaurant:logout')
    else:
        try:
            restaurant = User.objects.get(id=3)
        except:
            restaurant = User.objects.get(id=1)
        restaurant_name = restaurant.name

        try:
            # hiddenで取得したランダムコードがセッションに保存されたものと一致しているかチェック
            if random_code == request.session['nonloginuser'][table_num]:

                random_code = non_login_user_random_code(50)
                # セッションに保存されているランダムコードの更新
                request.session['nonloginuser'] = {table_num: random_code}
        except:
            messages.info(request, f'異常なエラーが発生しました。')
            return redirect('customer:table')

        try:
            from .models import Cart, Order
            users_cart = Cart.objects.filter(customer=uuid).order_by('-id')
            user_uuid = nonLoginUser.objects.get(uuid=uuid)

            # cartからorderにコピー
            for each in users_cart:
                order = Order(status='調理中', menu=each.menu,
                              num=each.num, customer=user_uuid)
                order.save()

            # コピーし終わったcartは削除
            users_cart.delete()
        except:
            None

        ctx = {
            'random_code': random_code,
            'restaurant_name': restaurant_name,
            'table_num': table_num,
            'categories': categories,
            'menus': menus,
        }

        messages.info(request, f"注文を承りました。今しばらくお待ちください")

        return render(request, 'customer/menu.html', ctx)


@require_POST
def history(request):
    user = request.user
    random_code = request.POST.get('random_code')
    table_num = request.POST.get('table')
    uuid = request.session['nonloginuser_uuid'][table_num]

    if user.is_authenticated:
        return redirect('restaurant:logout')
    else:

        try:
            # hiddenで取得したランダムコードがセッションに保存されたものと一致しているかチェック
            if random_code == request.session['nonloginuser'][table_num]:

                random_code = non_login_user_random_code(50)
                # セッションに保存されているランダムコードの更新
                request.session['nonloginuser'] = {table_num: random_code}
        except:
            messages.info(request, f'異常なエラーが発生しました。')
            return redirect('customer:table')

        from .models import Cart, Order
        user_uuid = nonLoginUser.objects.get(uuid=uuid)
        carts = Cart.objects.filter(customer=user_uuid).order_by('-id')
        orders = Order.objects.filter(customer=user_uuid).order_by('-id')
        # _orders = Order.objects.filter(
        #     (Q(status='キャンセル') | Q(status='済')), customer=user)

        in_cart_each_price = 0
        in_order_each_price = 0

        # TODO:
        # for i in orders_in_cart:
        #     in_cart_each_price += 700 * int(orders_in_cart[i].num)

        # for i in orders_in_order:
        #     in_order_each_price += 700 * int(orders_in_order[i].num)

        # print(in_cart_each_price)
        # print(in_order_each_price)

        total_price = in_cart_each_price + in_order_each_price

        ctx = {
            'random_code': random_code,
            'table_num': table_num,
            'carts': carts,
            'orders': orders,
            'total_price': total_price,
        }

        return render(request, 'customer/history.html', ctx)
