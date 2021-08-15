from django.contrib import admin
from .models import Category, Allergy, Option, Menu, Nomiho


# Register your models here.
class categoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'nomiho', 'created_at')
    list_editable = ('name', 'nomiho')
    ordering = ('id',)


class allergyAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'created_at')
    list_editable = ('ingredient',)
    ordering = ('id',)


class optionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'created_at')
    list_editable = ('name', 'price',)
    ordering = ('id',)


class menuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price',
                    'img', 'chef_img', 'comment', 'created_at')
    list_editable = ('name', 'category', 'price', 'img', 'chef_img', 'comment')
    ordering = ('id',)


class nomihoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'duration', 'comment', 'created_at')
    list_editable = ('name', 'price', 'duration', 'comment')
    ordering = ('id',)


admin.site.register(Category, categoryAdmin)
admin.site.register(Allergy, allergyAdmin)
admin.site.register(Option, optionAdmin)
admin.site.register(Menu, menuAdmin)
admin.site.register(Nomiho, nomihoAdmin)
