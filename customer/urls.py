from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'customer'
urlpatterns = [
    path('/table', views.table, name='table'),
]
