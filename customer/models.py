from django.db import models
from django.db.models.base import Model
from restaurant.models import Menu


# Create your models here.
class Order(models.Model):
    status = models.CharField("ステータス", max_length=256, blank=True, null=True)
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    table = models.PositiveIntegerField("テーブルの番号", blank=True, null=True)
    created_at = models.DateTimeField("オーダー発生時刻", auto_now=True)
