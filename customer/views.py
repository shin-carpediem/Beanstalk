from django.db.models import Sum
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404, redirect, render
from account.models import User, nonLoginUser
from restaurant.models import Allergy, Category, Menu
from .forms import ChooseTableForm, AddToCartForm


# Create your views here.
def restaurant_name():
    try:
        restaurant = User.objects.get(id=2)
    except:
        restaurant = User.objects.get(id=1)
    restaurant_name = restaurant.name
    return restaurant_name


def table(request):
    choose_table_form = ChooseTableForm(request.POST or None)
    restaurant_name()

    ctx = {
        'choose_table_form': choose_table_form,
        'restaurant_name': restaurant_name,
    }
    return render(request, 'customer/table.html', ctx)


def menu(request):
    name = request.POST.get('name')
    table = request.POST.get('table')

    try:
        session = Session.objects.get(pk=request.session.session_key)
    except Session.DoesNotExist:
        session = request.session.create()

    newuser = nonLoginUser(name=name, table=table, session=session,)
    newuser.save()

    restaurant_name()

    categories = Category.objects.all().order_by('id')
    first_category = Category(id=2)
    menus = Menu.objects.filter(category=first_category).order_by('-id')

    ctx = {
        'restaurant_name': restaurant_name,
        'table': table,
        'categories': categories,
        'menus': menus,
    }

    return render(request, 'customer/menu.html', ctx)


# TODO: 要更新
def table_num(request):
    user = request.non_login_user
    table_num = user.table
    ctx = {
        'table_num': table_num
    }
    return render(request, '*', ctx)


def category_filter(requset):
    category_name = requset.POST.get('category')
    category_id = Category.objects.get(name=category_name)

    restaurant_name()

    categories = Category.objects.all().order_by('id')
    menus = Menu.objects.filter(category=category_id).order_by('-id')

    ctx = {
        'restaurant_name': restaurant_name,
        'table': table_num,
        'categories': categories,
        'menus': menus,
    }

    return render(requset, 'customer/menu.html', ctx)


def menu_detail(request, menu_id):
    menu = get_object_or_404(Menu, pk=menu_id)
    allergies = Allergy.objects.all().order_by('id')
    has_allergies = menu.allergies.all().order_by('id')

    add_to_cart_form = AddToCartForm()

    ctx = {
        'menu': menu,
        'allergies': allergies,
        'has_allergies': has_allergies,
        'add_to_cart_form': add_to_cart_form,
    }
    return render(request, 'customer/detail.html', ctx)


def cart(request):
    from .models import Cart

    try:
        cart_num = request.POST.get('cart_num')
        menu_id = request.POST.get('menu_id')
        menu_instance = Menu.objects.get(id=menu_id)
        user = nonLoginUser.objects.get(id=request.user.id)
        cart = Cart(menu=menu_instance, num=cart_num, customer=user)
        cart.save()

    # メニュー画面から見るルート
    except:
        None

    carts = Cart.objects.all().order_by('-id')
    ctx = {
        'carts': carts,
    }

    return render(request, 'customer/cart.html', ctx)


def cart_detail(request, menu_id):
    menu = get_object_or_404(Menu, pk=menu_id)
    allergies = Allergy.objects.all().order_by('id')
    has_allergies = menu.allergies.all().order_by('id')

    ctx = {
        'menu': menu,
        'allergies': allergies,
        'has_allergies': has_allergies,
    }
    return render(request, 'customer/detail.html', ctx)


def order(request):
    user = nonLoginUser.objects.get(id=request.user.id)
    from .models import Cart, Order
    users_cart = Cart.objects.filter(customer=user).order_by('-id')
    print(users_cart)

    # cartからorderにコピー
    for each in users_cart:
        order = Order(status='調理中', menu=each.menu,
                      num=each.num, customer=user)
        order.save()

    # コピーし終わったcartは削除
    users_cart.delete()

    return redirect('customer:menu')


def history(request):
    user = nonLoginUser.objects.get(id=request.user.id)
    from .models import Cart, Order
    orders = Order.objects.all().order_by('-id')

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
        'orders': orders,
        'orders_in_cart': orders_in_cart,
        'orders_in_order': orders_in_order,
        'total_price': total_price,
    }
    return render(request, 'customer/history.html', ctx)
