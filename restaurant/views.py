from django.shortcuts import render
from .forms import LoginForm
from account.models import User


# Create your views here.
def login(request):
    form = LoginForm(request.POST or None)
    user = User.objects.get(id=2)
    formatted_logo = user.formatted_logo
    name = user.name
    ctx = {
        'form': form,
        'formatted_logo': formatted_logo,
        'name': name,
    }
    return render(request, 'restaurant/login.html', ctx)


def order_manage(request):
    return render(request, 'restaurant/order_manage.html')
