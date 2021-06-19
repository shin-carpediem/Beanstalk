from django.shortcuts import render
import django_filters
from rest_framework import viewsets, filters
from django.views.generic import View
from django.http import JsonResponse
from account.models import User, nonLoginUser
from customer.models import Cart, Order
from restaurant.models import Category, Allergy, Menu
from .serializer import UserSerializer, NonLoginUserSerializer, CartSerializer, OrderSerializer, CategorySerializer, AllergySerializer, MenuSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class NonLoginUserViewSet(viewsets.ModelViewSet):
    queryset = nonLoginUser.objects.all()
    serializer_class = NonLoginUserSerializer


class CartUserViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AllergyViewSet(viewsets.ModelViewSet):
    queryset = Allergy.objects.all()
    serializer_class = AllergySerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
