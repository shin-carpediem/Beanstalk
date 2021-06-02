from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'customer'
urlpatterns = [
    path('', views.table, name='table'),
    path('menu/', views.menu, name='menu'),
    path('history/', views.history, name='history'),
]
