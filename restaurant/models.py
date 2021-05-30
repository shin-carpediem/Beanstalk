from django.db import models


# Create your models here.
class Menu(models.Model):
    name = models.CharField("表示名", max_length=256, blank=True, null=True)
    category = models.CharField("カテゴリ", max_length=256, blank=True, null=True)
    price = models.PositiveIntegerField("価格", blank=True, null=True)
    img = models.FileField("イメージ画像", blank=True, null=True)
    allergies = models.CharField("アレルギー", max_length=256, blank=True, null=True)
    created_at = models.DateTimeField("作成日", auto_now=True)
