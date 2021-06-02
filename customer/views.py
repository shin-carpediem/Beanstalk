from django.contrib import messages
from django.contrib.sessions.models import Session
from django.shortcuts import render
from account.models import User, nonLoginUser
from .forms import ChooseTableForm


def restaurant_name():
    try:
        restaurant_name = User.objects.get(id=2)
    except:
        restaurant_name = User.objects.get(id=1)
    return restaurant_name


# Create your views here.
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
    ctx = {
        'restaurant_name': restaurant_name,
        'table': table,
    }

    return render(request, 'customer/menu.html', ctx)


def menu_detail(request, pk):
    return render(request, 'customer/detail.html')


def cart(request):
    return render(request, 'customer/cart.html')


def cart_detail(request, pk):
    return render(request, 'customer/detail.html')


def history(request):
    return render(request, 'customer/history.html')
