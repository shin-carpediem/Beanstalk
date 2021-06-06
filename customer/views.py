from django.db.models import Sum
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404, redirect, render
from account.models import User, nonLoginUser
from restaurant.models import Allergy, Category, Menu
from .forms import ChooseTableForm, AddToCartForm


# Create your views here.
def table(request):
    choose_table_form = ChooseTableForm(request.POST or None)

    try:
        restaurant = User.objects.get(id=2)
    except:
        restaurant = User.objects.get(id=1)
    restaurant_name = restaurant.name

    ctx = {
        'choose_table_form': choose_table_form,
        'restaurant_name': restaurant_name,
    }
    return render(request, 'customer/table.html', ctx)


def make_session(request):
    name = request.POST.get('name')
    table = request.POST.get('table')

    try:
        session = Session.objects.get(pk=request.session.session_key)
    # create new session
    except Session.DoesNotExist:
        session = request.session.create()

    newuser = nonLoginUser(name=name, table=table, session=session,)
    newuser.save()

    try:
        restaurant = User.objects.get(id=2)
    except:
        restaurant = User.objects.get(id=1)
    restaurant_name = restaurant.name

    name = request.POST.get('name')
    table = request.POST.get('table')

    categories = Category.objects.all().order_by('id')
    first_category = Category(id=2)
    menus = Menu.objects.filter(category=first_category).order_by('-id')

    ctx = {
        'name': name,
        'table': table,
        'restaurant_name': restaurant_name,
        'table': table,
        'categories': categories,
        'menus': menus,
    }

    return render(request, 'customer/menu.html', ctx)


def menu(request):
    try:
        restaurant = User.objects.get(id=2)
    except:
        restaurant = User.objects.get(id=1)
    restaurant_name = restaurant.name

    name = request.POST.get('name')
    table = request.POST.get('table')

    session = Session.objects.get(pk=request.session.session_key)
    user = nonLoginUser.objects.get(session=session)

    table_num = user.table

    categories = Category.objects.all().order_by('id')
    first_category = Category(id=2)
    menus = Menu.objects.filter(category=first_category).order_by('-id')

    ctx = {
        'name': name,
        'table': table,
        'restaurant_name': restaurant_name,
        'table_num': table_num,
        'categories': categories,
        'menus': menus,
    }

    return render(request, 'customer/menu.html', ctx)


def category_filter(request):
    try:
        restaurant = User.objects.get(id=2)
    except:
        restaurant = User.objects.get(id=1)
    restaurant_name = restaurant.name

    session = Session.objects.get(pk=request.session.session_key)
    user = nonLoginUser.objects.get(session=session)

    table_num = user.table

    category_name = request.POST.get('category')
    category_id = Category.objects.get(name=category_name)

    categories = Category.objects.all().order_by('id')
    menus = Menu.objects.filter(category=category_id).order_by('-id')

    ctx = {
        'restaurant_name': restaurant_name,
        'table_num': table_num,
        'categories': categories,
        'menus': menus,
    }

    return render(request, 'customer/menu.html', ctx)


def menu_detail(request, menu_id):
    session = Session.objects.get(pk=request.session.session_key)
    user = nonLoginUser.objects.get(session=session)

    table_num = user.table

    menu = get_object_or_404(Menu, pk=menu_id)
    allergies = Allergy.objects.all().order_by('id')
    has_allergies = menu.allergies.all().order_by('id')

    add_to_cart_form = AddToCartForm()

    ctx = {
        'menu': menu,
        'table_num': table_num,
        'allergies': allergies,
        'has_allergies': has_allergies,
        'add_to_cart_form': add_to_cart_form,
    }
    return render(request, 'customer/detail.html', ctx)


def cart(request):
    session = Session.objects.get(pk=request.session.session_key)
    user = nonLoginUser.objects.get(session=session)

    table_num = user.table

    from .models import Cart

    # メニューの詳細から見るルート
    try:
        menu_id = request.POST.get('menu_id')

        menu_instance = Menu.objects.get(id=menu_id)
        cart_num = request.POST.get('cart_num')

        cart = Cart(menu=menu_instance, num=cart_num, customer=user)
        cart.save()

    # メニュー画面から見るルート
    except:
        None

    carts = Cart.objects.all().order_by('-id')
    ctx = {
        'table_num': table_num,
        'carts': carts,
    }

    return render(request, 'customer/cart.html', ctx)


def cart_detail(request, menu_id):
    session = Session.objects.get(pk=request.session.session_key)
    user = nonLoginUser.objects.get(session=session)

    table_num = user.table

    menu = get_object_or_404(Menu, pk=menu_id)
    allergies = Allergy.objects.all().order_by('id')
    has_allergies = menu.allergies.all().order_by('id')

    add_to_cart_form = AddToCartForm()

    ctx = {
        'table_num': table_num,
        'menu': menu,
        'allergies': allergies,
        'has_allergies': has_allergies,
        'add_to_cart_form': add_to_cart_form,
    }
    return render(request, 'customer/detail.html', ctx)


def order(request):
    try:
        session = Session.objects.get(pk=request.session.session_key)
        user = nonLoginUser.objects.get(session=session)

        from .models import Cart, Order
        users_cart = Cart.objects.filter(customer=user).order_by('-id')

        # cartからorderにコピー
        for each in users_cart:
            order = Order(status='調理中', menu=each.menu,
                          num=each.num, customer=user)
            order.save()

        # コピーし終わったcartは削除
        users_cart.delete()

        messages.success(
            request, f"注文を承りました。今しばらくお待ちください"
        )

    except:
        None

        return redirect('customer:menu')


def history(request):
    session = Session.objects.get(pk=request.session.session_key)
    user = nonLoginUser.objects.get(session=session)

    table_num = user.table

    add_to_cart_form = AddToCartForm()

    from .models import Cart, Order
    carts = Cart.objects.filter(customer=user).order_by('-id')
    orders = Order.objects.filter(customer=user).order_by('-id')

    orders_in_cart = Cart.objects.filter(customer=user)
    orders_in_order = Order.objects.filter(status='調理中', customer=user)

    in_cart_each_price = 0
    in_order_each_price = 0

    # for i in orders_in_cart:
    #     in_cart_each_price += 700 * int(orders_in_cart[i].num)

    # for i in orders_in_order:
    #     in_order_each_price += 700 * int(orders_in_order[i].num)

    print(in_cart_each_price)
    print(in_order_each_price)

    total_price = in_cart_each_price + in_order_each_price

    ctx = {
        'table_num': table_num,
        'carts': carts,
        'orders': orders,
        'orders_in_cart': orders_in_cart,
        'orders_in_order': orders_in_order,
        'total_price': total_price,
        'add_to_cart_form': add_to_cart_form,
    }
    return render(request, 'customer/history.html', ctx)
