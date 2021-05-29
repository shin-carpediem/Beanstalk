from django.shortcuts import render


# Create your views here.
def order_manage(request):
    return render(request, 'restaurant/order_manage.html')
