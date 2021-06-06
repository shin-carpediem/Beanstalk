from django import forms
from django.db import models
from django.forms import fields
from .models import Category, Allergy, Menu


class AddCategoryForm(forms.Form):
    class Meta:
        model = Category
        label = '追加'
        fields = ('name',)


class AddAllergyForm(forms.Form):
    class Meta:
        model = Allergy
        fields = ('ingredient',)


class AddMenuForm(forms.Form):
    class Meta:
        model = Menu
        fields = ('name', 'category', 'price', 'img', 'allergies',)
