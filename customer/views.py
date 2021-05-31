from django.contrib import messages
from django.contrib.sessions.models import Session
from django.shortcuts import render
from account.models import User, nonLoginUser
from .forms import ChooseTableForm


# Create your views here.
def table(request):
    choose_table_form = ChooseTableForm(request.POST or None)
    try:
        restaurant_name = User.objects.get(id=2)
    except:
        restaurant_name = User.objects.get(id=1)

    if request.method == 'POST':
        name = request.POST.get('name')
        table = request.POST.get('table')
        try:
            session = Session.objects.get(pk=request.session.session_key)
        except Session.DoesNotExist:
            session = request.session.create()
        newuser = nonLoginUser(name=name, table=table, session=session,)
        newuser.save()
        return render(request, 'customer/menu.html')

    ctx = {
        'choose_table_form': choose_table_form,
        'restaurant_name': restaurant_name,
    }
    return render(request, 'customer/table.html', ctx)


def history(request):
    return render(request, 'customer/history.html')
