from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from account.models import User


# Create your views here.
def order_manage(request):
    return render(request, 'restaurant/order_manage.html')

# def login(request):
#     form = LoginForm(request.POST or None)
#     user = User.objects.get(id=2)
#     formatted_logo = user.formatted_logo
#     name = user.name

#     if request.method == 'POST':
#         password = form.cleaned_data['password']
#         print(password)
#         request_password = request.POST.get('password')
#         if password == request_password:
#             login(request, user)
#             return render(request, 'restaurant/order_manage.html')
#         else:
#             messages.warning(request, f"パスワードが違います。")
#             return redirect('restaurant:login')

#     ctx = {
#         'form': form,
#         'formatted_logo': formatted_logo,
#         'name': name,
#     }
#     return render(request, 'restaurant/login.html', ctx)