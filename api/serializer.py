from django.db.models import fields
from rest_framework import serializers
from account.models import User, nonLoginUser
from customer.models import Cart, Order
from restaurant.models import Category, Allergy, Menu


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'logo',
                  'is_staff', 'is_active', 'date_joined')


class NonLoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = nonLoginUser
        fields = ('uuid', 'table', 'created_at')


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'menu', 'num', 'customer', 'created_at')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'status', 'menu', 'num', 'customer', 'created_at')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'created_at')


class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = ('id', 'ingredient', 'created_at')


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'name', 'category', 'price',
                  'img', 'allergies', 'created_at')


class NomihoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'name', 'price', 'menu', 'created_at')
