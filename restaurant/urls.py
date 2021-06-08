from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'restaurant'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='restaurant/login.html'), name='login'),
    path('order_manage/', views.order_manage, name='order_manage'),
    path('order_manage/history/', views.history, name='history'),
    path('manage/login/', views.manage_login, name='manage_login'),
    path('manage/menu/', views.manage_menu, name='manage_menu'),
    path('manage/menu/', views.category_add, name='category_add'),
    path('manage/menu/', views.category_ch, name='category_ch'),
    path('manage/menu/', views.category_del, name='category_del'),
    path('manage/menu/detail/', views.menu_img_manage, name='menu_img_manage'),
    path('manage/menu/detail/', views.menu_name_manage, name='menu_name_manage'),
    path('manage/menu/detail/', views.menu_price_manage, name='menu_price_manage'),
    path('manage/menu/detail/', views.allergy_add, name='allergy_add'),
    path('manage/menu/detail/', views.allergy_ch, name='allergy_ch'),
    path('manage/menu/detail/', views.allergy_del, name='allergy_del'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
