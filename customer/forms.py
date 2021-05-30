from django import forms
from django.forms import fields


class ChooseTableForm(forms.Form):
    num = forms.IntegerField(
        label='',
        min_value=1, required=True
    )
