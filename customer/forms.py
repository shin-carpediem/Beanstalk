from django import forms
from django.forms import fields


class ChooseTableForm(forms.Form):
    table = forms.IntegerField(
        label='テーブル番号',
        min_value=1,
        required=True
    )
