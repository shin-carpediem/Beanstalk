from django.contrib import admin
from .models import Category, Allergy, Menu, Nomiho


# Register your models here.
class categoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'nomiho', 'created_at')
    ordering = ('id',)


class allergyAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'created_at')
    ordering = ('id',)


class menuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price',
                    'img', 'created_at')
    ordering = ('id',)


class nomihoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'duration', 'comment', 'created_at')
    ordering = ('id',)


admin.site.register(Category, categoryAdmin)
admin.site.register(Allergy, allergyAdmin)
admin.site.register(Menu, menuAdmin)
admin.site.register(Nomiho, nomihoAdmin)
