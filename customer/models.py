from django.db import models
from django.db.models.base import Model
from restaurant.models import Menu


# Create your models here.
class Table(models.Model):
    table_num = models.PositiveIntegerField("テーブルの番号", blank=True, null=True)
    created_at = models.DateTimeField("作成日", auto_now=True)

    def __str__(self):
        return str(self.table_num)


class Order(models.Model):
    status = models.CharField("ステータス", max_length=256, blank=True, null=True)
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    table = models.ForeignKey(Table, on_delete=models.PROTECT)
    created_at = models.DateTimeField("オーダー発生時刻", auto_now=True)
