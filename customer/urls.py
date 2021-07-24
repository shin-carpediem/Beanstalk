from django.urls import path
from . import views


app_name = 'customer'
urlpatterns = [
    path('', views.index, name='index'),
    path('table/', views.table, name='table'),
    path('menu/', views.menu, name='menu'),
    path('filter/', views.filter, name='filter'),
    path('<int:menu_id>/detail/', views.menu_detail, name='menu_detail'),
    path('cart/', views.cart, name='cart'),
    path('cart/static/', views.cart_static, name='cart_static'),
    path('cart/<int:menu_id>/detail/', views.cart_detail, name='cart_detail'),
    path('cart/cart_ch/', views.cart_ch, name='cart_ch'),
    path('order/', views.order, name='order'),
    path('nomiho/', views.nomiho, name='nomiho'),
    path('history/', views.history, name='history'),
    path('stop/', views.stop, name='stop'),
    path('stop/static/', views.stop_static, name='stop_static'),
    path('revert/', views.revert, name='revert'),
    path('revert/index/', views.revert_from_index, name='revert_from_index'),
]
