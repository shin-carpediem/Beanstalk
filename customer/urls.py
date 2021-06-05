from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'customer'
urlpatterns = [
    path('', views.table, name='table'),
    path('menu/', views.menu, name='menu'),
    path('category_filter/', views.category_filter, name='category_filter'),
    path('<int:menu_id>/detail/', views.menu_detail, name='menu_detail'),
    path('cart/', views.cart, name='cart'),
    path('cart/<int:menu_id>/detail/', views.cart_detail, name='cart_detail'),
    path('order/', views.order, name='order'),
    path('history/', views.history, name='history'),
]
