from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from account.models import User
from .models import Allergy, Category, Menu


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

    categories = Category.objects.all().order_by('id')
    first_category = Category(id=2)
    menus = Menu.objects.filter(category=first_category).order_by('-id')

    ctx = {
        'restaurant_name': restaurant_name,
        'categories': categories,
        'menus': menus,
    }
    return render(request, 'customer/menu.html', ctx)
