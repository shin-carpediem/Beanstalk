from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from account.models import User


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
    return render(request, 'restaurant/manage/menu.html')
