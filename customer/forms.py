from django import forms
from django.forms import fields


class ChooseTableForm(forms.Form):
    name = forms.CharField(
        label='お名前',
        min_length=1,
        required=True
    )
    table = forms.IntegerField(
        label='テーブル番号',
        min_value=1,
        required=True
    )


class AddToCartForm(forms.Form):
    num = forms.IntegerField(
        label='',
        min_value=1,
        required=True
    )
