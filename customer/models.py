from customer.views import table
from django.db import models
from django.db.models.base import Model
from account.models import nonLoginUser
from restaurant.models import Menu


# Create your models here.
class Cart(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    num = models.PositiveIntegerField("個数", blank=True, null=True)
    customer = models.ForeignKey(nonLoginUser, on_delete=models.PROTECT)
    created_at = models.DateTimeField("カート追加時刻", auto_now=True)

    def __str__(self):
        return str(self.menu)


class Order(models.Model):
    status = models.CharField("ステータス", max_length=256, blank=True, null=True)
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    num = models.PositiveIntegerField("個数", blank=True, null=True)
    customer = models.ForeignKey(nonLoginUser, on_delete=models.PROTECT)
    created_at = models.DateTimeField("オーダー発生時刻", auto_now=True)

    def __str__(self):
        return str(self.status)
