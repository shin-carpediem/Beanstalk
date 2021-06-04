from django.contrib import messages
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404, render
from account.models import User, nonLoginUser
from restaurant.models import Category, Menu
from .forms import ChooseTableForm


# Create your views here.
def restaurant_name():
    try:
        restaurant_name = User.objects.get(id=2)
    except:
        restaurant_name = User.objects.get(id=1)
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
    menus = Menu.objects.all().order_by('-id')

    ctx = {
        'restaurant_name': restaurant_name,
        'table': table,
        'categories': categories,
        'menus': menus,
    }

    return render(request, 'customer/menu.html', ctx)


def category_filter(requset):
    category_name = requset.POST.get('category.name')
    print(category_name)

    restaurant_name()

    categories = Category.objects.all().order_by('id')
    menus = Menu.objects.filter(category=category_name).order_by('-id')

    ctx = {
        'restaurant_name': restaurant_name,
        # 'table': table,
        'categories': categories,
        'menus': menus,
    }

    return render(requset, 'customer/menu.html', ctx)


def menu_detail(request, menu_id):
    menu = get_object_or_404(Menu, pk=menu_id)
    ctx = {
        'menu': menu,
    }
    return render(request, 'customer/detail.html', ctx)


def cart(request):
    return render(request, 'customer/cart.html')


def cart_detail(request, menu_id):
    menu = get_object_or_404(Menu, pk=menu_id)
    ctx = {
        'menu': menu,
    }
    return render(request, 'customer/detail.html', ctx)


def history(request):
    return render(request, 'customer/history.html')
