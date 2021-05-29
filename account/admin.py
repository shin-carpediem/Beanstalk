from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.db.models import fields
from django.utils.translation import ugettext_lazy as _
from .models import User


# Register your models here.
class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name',)


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
                                       'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('name', 'last_login')
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(User, MyUserAdmin)
