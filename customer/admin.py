from django.contrib import admin
from .models import Cart, Order


# Register your models here.
class cartAdmin(admin.ModelAdmin):
    list_display = ('id', 'menu', 'num', 'curr', 'created_at')
    list_editable = ('menu', 'num', 'curr')
    ordering = ('-created_at',)


class orderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'menu', 'num',
                    'curr', 'created_at')
    list_editable = ('menu', 'num', 'curr')
    ordering = ('-created_at',)


admin.site.register(Cart, cartAdmin)
admin.site.register(Order, orderAdmin)
