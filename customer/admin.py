from django.contrib import admin
from .models import Cart, Order, NomihoOrder


# Register your models here.
class cartAdmin(admin.ModelAdmin):
    list_display = ('id', 'menu', 'num', 'request', 'curr', 'created_at')
    list_editable = ('menu', 'num', 'curr')
    ordering = ('-created_at',)


class orderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'menu', 'num', 'request',
                    'curr', 'created_at')
    list_editable = ('menu', 'num', 'curr')
    ordering = ('-created_at',)


class NomihoOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'nomiho', 'table', 'num',
                    'curr', 'created_at')
    list_editable = ('status', 'table', 'num', 'curr')
    ordering = ('-created_at',)


admin.site.register(Cart, cartAdmin)
admin.site.register(Order, orderAdmin)
admin.site.register(NomihoOrder, NomihoOrderAdmin)
