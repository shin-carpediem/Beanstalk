from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'restaurant'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='restaurant/login.html'), name='login'),
    path('order_manage/', views.order_manage, name='order_manage'),
    path('manage/login/', views.manage_login, name='manage_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
