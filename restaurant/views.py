from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from account.models import User
from customer.forms import AddToCartForm
from .models import Category, Allergy, Menu
from .forms import AddCategoryForm, AddAllergyForm, AddMenuForm, DelMenuForm


# Create your views here.
@login_required
def order_manage(request):
    user = User.objects.get(id=request.user.id)
    formatted_logo = user.formatted_logo
    name = user.name
    ctx = {
        'formatted_logo': formatted_logo,
        'name': name,
    }
    return render(request, 'restaurant/order_manage.html', ctx)


@login_required
def history(request):
    return render(request, 'restaurant/history.html')


# for manageing menu
def manage_login(request):
    return render(request, 'restaurant/login.html')


@login_required
def manage_menu(request):
    add_category_form = AddCategoryForm()
    add_menu_form = AddMenuForm()
    del_menu_form = DelMenuForm()

    user = request.user
    restaurant_name = user.name

    categories = Category.objects.all().order_by('id')
    first_category = Category(id=2)
    menus = Menu.objects.filter(category=first_category).order_by('-id')

    ctx = {
        'add_category_form': add_category_form,
        'add_menu_form': add_menu_form,
        'del_menu_form': del_menu_form,
        'restaurant_name': restaurant_name,
        'categories': categories,
        'menus': menus,
    }
    return render(request, 'customer/menu.html', ctx)


@login_required
@require_POST
def category_manage(request):
    return render(request, 'customer/menu.html')


@login_required
@require_POST
def menu_img_manage(request):
    menu_img = request.FILES.get('menu_img')
    menu_id = request.POST.get('menu_id')
    menu = Menu.objects.get(id=menu_id)

    # 以前のファイルは削除
    menu.img.delete(False)

    menu.img = menu_img
    menu.save()

    table_num = "管理者"

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


@login_required
@require_POST
def menu_name_manage(request):
    menu_name = request.POST.get('menu_name')
    menu_id = request.POST.get('menu_id')
    menu = Menu.objects.get(id=menu_id)
    menu.name = menu_name
    menu.save()

    table_num = "管理者"

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


@login_required
@require_POST
def menu_price_manage(request):
    menu_price = request.POST.get('menu_price')
    menu_id = request.POST.get('menu_id')
    menu = Menu.objects.get(id=menu_id)
    menu.price = menu_price
    menu.save()

    table_num = "管理者"

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
