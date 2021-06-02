from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'customer'
urlpatterns = [
    path('', views.table, name='table'),
    path('menu/', views.menu, name='menu'),
    path('<pk>/detail/', views.menu_detail, name='menu_detail'),
    path('cart/', views.cart, name='cart'),
    path('cart/<pk>/detail/', views.cart_detail, name='cart_detail'),
    path('history/', views.history, name='history'),
]
