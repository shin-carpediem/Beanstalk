from django import forms
from django.forms import fields
from account.models import User


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('password',)
