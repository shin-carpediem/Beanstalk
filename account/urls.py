from django.urls import path
from . import views


app_name = 'account'
urlpatterns = [
    path('terms/', views.terms, name='terms'),
    path('policy/', views.policy, name='policy'),
]
