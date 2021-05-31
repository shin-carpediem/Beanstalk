from django.contrib import admin
from .models import Category, Allergy, Menu


# Register your models here.
admin.site.register(Category)
admin.site.register(Allergy)
admin.site.register(Menu)
