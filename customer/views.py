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


def table_num(request):
    user = request.non_login_user
    table_num = user.table
    ctx = {
        'table_num': table_num
    }
    return render(request, '*', ctx)


# TODO: フォームを使う
def category_filter(requset):
    category_name = requset.POST.get('category')
    print(category_name)

    restaurant_name()
    table_num()

    categories = Category.objects.all().order_by('id')
    menus = Menu.objects.filter(category=category_name).order_by('-id')

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
    cart_num = request.POST.get('cart_num')
    menu_id = request.POST.get('menu_id')
    menu_instance = Menu.objects.get(id=menu_id)
    user = nonLoginUser.objects.get(id=request.user.id)

    from .models import Cart
    cart = Cart(menu=menu_instance, num=cart_num, customer=user)
    cart.save()
    carts = Cart.objects.all().order_by('-id')

    ctx = {
        'carts': carts,
        'cart_num': cart_num,
        'menu_id': menu_id,
        'menu_instance': menu_instance,
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


# TODO:
def order(request):
    user = nonLoginUser.objects.get(id=request.user.id)
    from .models import Cart, Order
    users_cart = Cart.objects.filter(customer=user).order_by('-id')
    # for each in users_cart:

    # Order(menu=menu_instance, num=order_num, customer=user)

    return redirect('customer:menu')


def history(request):
    return render(request, 'customer/history.html')
