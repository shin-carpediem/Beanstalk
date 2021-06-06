from django import forms
from django.db import models
from django.forms import fields
from .models import Category, Allergy, Menu


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        label = '追加'
        fields = ('name',)


class AddAllergyForm(forms.ModelForm):
    class Meta:
        model = Allergy
        fields = ('ingredient',)


class AddMenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ('name', 'category', 'price', 'img', 'allergies',)


class ChooseCategoryForm(forms.Form):
    name = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label='選択してください')


class ChooseAllergyForm(forms.Form):
    name = forms.ModelChoiceField(
        queryset=Allergy.objects.all(), empty_label='選択してください')


class ChooseMenuForm(forms.Form):
    name = forms.ModelChoiceField(
        queryset=Menu.objects.all(), empty_label='選択してください')
