from django.http import request
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Category, Allergy, Menu
from account.models import User
from beanstalk.settings import DEBUG


# Create your views here.
# default
table_num = '管理者'
categories = Category.objects.all().order_by('id')
first_category = Category(id=2)
menus = Menu.objects.filter(category=first_category).order_by('-id')
allergies = Allergy.objects.all().order_by('id')
ctx = {
    'table_num': table_num,
    'categories': categories,
    'menus': menus,
    'allergies': allergies,
}


@login_required
def order_manage(request):
    # table_num = '管理者'
    # categories = Category.objects.all().order_by('id')
    # first_category = Category(id=2)
    # menus = Menu.objects.filter(category=first_category).order_by('-id')
    # allergies = Allergy.objects.all().order_by('id')
    # ctx = {
    #     'table_num': table_num,
    #     'categories': categories,
    #     'menus': menus,
    #     'allergies': allergies,
    # }

    user = User.objects.get(id=request.user.id)
    formatted_logo = user.formatted_logo
    name = user.name
    ctx['formatted_logo'] = formatted_logo
    ctx['name'] = name,

    return render(request, 'restaurant/order_manage.html', ctx)


@login_required
def history(request):
    return render(request, 'restaurant/history.html')


# for manageing menu
def manage_login(request):
    return render(request, 'restaurant/login.html')


def password_reset(request):
    if DEBUG:
        return redirect('http://127.0.0.1:8000/admin/password_reset/')
    # TODO:
    else:
        return redirect('https://xxx.com/admin/password_reset/')


@login_required
def manage_menu(request):
    # table_num = '管理者'
    # categories = Category.objects.all().order_by('id')
    # first_category = Category(id=2)
    # menus = Menu.objects.filter(category=first_category).order_by('-id')
    # allergies = Allergy.objects.all().order_by('id')
    # ctx = {
    #     'table_num': table_num,
    #     'categories': categories,
    #     'menus': menus,
    #     'allergies': allergies,
    # }

    user = request.user
    restaurant_name = user.name
    ctx['restaurant_name'] = restaurant_name

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

    return redirect('customer:menu')


@login_required
@require_POST
def category_ch(request):
    name = request.POST.get('category_name')
    required_name = request.POST.get('ch_category_form')
    category = Category.objects.get(name=name)
    category.name = required_name
    category.save()

    return redirect('customer:menu')


@login_required
@require_POST
def category_del(request):
    name = request.POST.get('del_category_form')
    try:
        category = Category.objects.get(name=name)
        category.delete()
    except:
        messages.warning(request, f"削除に失敗しました。")

    return redirect('customer:menu')


@login_required
@require_POST
def menu_add(request):
    name = request.POST.get('name')
    if Menu.objects.filter(name=name).count() != 0:
        messages.warning(request, f"全く同じ名前のメニューは作れません。")

    else:
        category = request.POST.get('category')
        # foreign_key
        category_id = Category.objects.get(name=category)
        price = request.POST.get('price')
        img = request.FILES.get('img')

        menu = Menu(name=name, category=category_id,
                    price=price, img=img)
        menu.save()

        allergy_list = request.POST.getlist('allergy')
        for allergy in allergy_list:
            allergy_query = Allergy.objects.get(ingredient=allergy)
            print(allergy_query)
            menu.allergies.add(allergy_query)

        menu.save()

    return redirect('customer:menu')


@login_required
@require_POST
def menu_del(request):
    required_menu = request.POST.get('menu')
    menu = Menu.objects.get(name=required_menu)
    menu.delete()

    return redirect('customer:menu')


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

    return redirect('customer:menu_detail', menu_id=menu.id)


@login_required
@require_POST
def menu_name_manage(request):
    menu_name = request.POST.get('menu_name')
    menu_id = request.POST.get('menu_id')
    print(menu_id)
    menu = Menu.objects.get(id=menu_id)
    menu.name = menu_name
    menu.save()

    return redirect('customer:menu_detail', menu_id=menu.id)


@login_required
@require_POST
def menu_price_manage(request):
    menu_price = request.POST.get('menu_price')
    menu_id = request.POST.get('menu_id')
    menu = Menu.objects.get(id=menu_id)
    menu.price = menu_price
    menu.save()

    return redirect('customer:menu_detail', menu_id=menu.id)


@login_required
@require_POST
def allergy_ch(request):
    allergy_list = request.POST.getlist('allergy')
    menu_id = request.POST.get('menu_id')

    menu = Menu.objects.get(id=menu_id)
    for allergy in allergy_list:
        # データと変わらない場合は何もしない
        if allergy in menu.allergies.all():
            None
        # 新しくチェックをつけたものは登録する
        else:
            allergy_query = Allergy.objects.get(ingredient=allergy)
            menu.allergies.add(allergy_query)

    menu.save()

    menu = Menu.objects.get(id=menu_id)
    for allergy in menu.allergies.all():
        # チェックされているものとデータが同じ場合は何もしない
        if allergy.ingredient in allergy_list:
            None
        # 新しくチェックを外したものはデータからも外す
        else:
            allergy_query = Allergy.objects.get(ingredient=allergy)
            menu.allergies.remove(allergy_query)

    menu.save()

    return redirect('customer:menu')


@login_required
@require_POST
def allergy_add(request):
    get_allergy = request.POST.get('allergy')
    menu_id = request.POST.get('menu_id')
    menu = Menu.objects.get(id=menu_id)
    menu.allergies.create(ingredient=get_allergy)
    menu.save()

    return redirect('customer:menu')


@login_required
@require_POST
def allergy_del(request):
    get_allergy = request.POST.get('allergy')
    allergy = Allergy.objects.get(ingredient=get_allergy)
    allergy.delete()

    return redirect('customer:menu')
