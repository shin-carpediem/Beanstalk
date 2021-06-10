from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from account.models import User
from customer.forms import AddToCartForm
from .models import Category, Allergy, Menu


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
    user = request.user
    restaurant_name = user.name

    table_num = '管理者'

    categories = Category.objects.all().order_by('id')
    first_category = Category(id=2)
    menus = Menu.objects.filter(category=first_category).order_by('-id')

    allergies = Allergy.objects.all().order_by('id')

    ctx = {
        'restaurant_name': restaurant_name,
        'table_num': table_num,
        'categories': categories,
        'menus': menus,
        'allergies': allergies,
    }
    return render(request, 'customer/menu.html', ctx)


@login_required
@require_POST
def category_add(request):
    name = request.POST.get('add_category_form')
    if Category.objects.filter(name=name).count() == 0:
        category = Category(name=name)
        category.save()
    else:
        messages.warning(request, f"同じ名前のカテゴリは作成できません。")

    user = request.user
    restaurant_name = user.name

    table_num = '管理者'

    categories = Category.objects.all().order_by('id')
    first_category = Category(id=2)
    menus = Menu.objects.filter(category=first_category).order_by('-id')

    ctx = {
        'restaurant_name': restaurant_name,
        'table_num': table_num,
        'categories': categories,
        'menus': menus,
    }

    return render(request, 'customer/menu.html', ctx)


@login_required
@require_POST
def category_ch(request):
    name = request.POST.get('category_name')
    required_name = request.POST.get('ch_category_form')
    try:
        category = Category.objects.get(name=name)
        category.name = required_name
        print(category.name)
        category.save()
    except:
        messages.warning(request, f"変更に失敗しました。")

    user = request.user
    restaurant_name = user.name

    table_num = '管理者'

    categories = Category.objects.all().order_by('id')
    first_category = Category(id=2)
    menus = Menu.objects.filter(category=first_category).order_by('-id')

    ctx = {
        'restaurant_name': restaurant_name,
        'table_num': table_num,
        'categories': categories,
        'menus': menus,
    }
    return render(request, 'customer/menu.html', ctx)


@login_required
@require_POST
def category_del(request):
    name = request.POST.get('del_category_form')
    try:
        category = Category.objects.get(name=name)
        category.delete(False)
    except:
        messages.warning(request, f"削除に失敗しました。")

    user = request.user
    restaurant_name = user.name

    table_num = '管理者'

    categories = Category.objects.all().order_by('id')
    first_category = Category(id=2)
    menus = Menu.objects.filter(category=first_category).order_by('-id')

    ctx = {
        'restaurant_name': restaurant_name,
        'table_num': table_num,
        'categories': categories,
        'menus': menus,
    }
    return render(request, 'customer/menu.html', ctx)


@login_required
@require_POST
def menu_add(request):
    name = request.POST.get('name')
    category = request.POST.get('category')
    # foreign_key
    category_id = Category.objects.get(name=category)
    price = request.POST.get('price')
    img = request.POST.get('img')
    # allergy = request.POST.get('allergy')
    # allergy_list = []
    # allergy_list.set(allergy)
    # many_to_many
    # allergy_ids = Allergy.objects.get(ingredient=allergy_list)
    menu = Menu(name=name, category=category_id,
                price=price, img=img)
    menu.save()

    user = request.user
    restaurant_name = user.name

    table_num = '管理者'

    categories = Category.objects.all().order_by('id')
    first_category = Category(id=2)
    menus = Menu.objects.filter(category=first_category).order_by('-id')

    allergies = Allergy.objects.all().order_by('id')

    ctx = {
        'restaurant_name': restaurant_name,
        'table_num': table_num,
        'categories': categories,
        'menus': menus,
        'allergies': allergies,
    }
    return render(request, 'customer/menu.html', ctx)


@login_required
@require_POST
def menu_del(request):
    required_menu = request.POST.get('menu')
    menu = Menu.objects.get(name=required_menu)
    menu.delete()

    user = request.user
    restaurant_name = user.name

    table_num = '管理者'

    categories = Category.objects.all().order_by('id')
    first_category = Category(id=2)
    menus = Menu.objects.filter(category=first_category).order_by('-id')

    allergies = Allergy.objects.all().order_by('id')

    ctx = {
        'restaurant_name': restaurant_name,
        'table_num': table_num,
        'categories': categories,
        'menus': menus,
        'allergies': allergies,
    }
    return render(request, 'customer/menu.html', ctx)


@login_required
@require_POST
def menu_img_manage(request):
    menu_img = request.FILES.get('menu_img')
    menu_id = request.POST.get('menu_id')
    menu = Menu.objects.get(id=menu_id)
    print(menu)

    # 以前のファイルは削除
    menu.img.delete(False)

    menu.img = menu_img
    menu.save()

    table_num = '管理者'

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


@login_required
@require_POST
def menu_name_manage(request):
    menu_name = request.POST.get('menu_name')
    menu_id = request.POST.get('menu_id')
    menu = Menu.objects.get(id=menu_id)
    menu.name = menu_name
    menu.save()

    table_num = '管理者'

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

    table_num = '管理者'

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
def allergy_add(request):
    name = request.POST.get('add_allergy_form')
    menu_id = request.POST.get('menu_id')

    menu = Menu.objects.get(id=menu_id)
    menu.allergy = name
    menu.save()

    table_num = '管理者'

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
    return render(request, 'customer/menu.html', ctx)


@login_required
@require_POST
def allergy_ch(request):
    return render(request, 'customer/menu.html')


@login_required
@require_POST
def allergy_del(request):
    return render(request, 'customer/menu.html')
