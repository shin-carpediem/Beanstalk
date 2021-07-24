from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.
class Category(models.Model):
    name = models.CharField("カテゴリ", max_length=256, blank=True, null=True)
    nomiho = models.BooleanField(
        "飲み放題用カテゴリ", default=False, blank=True, null=True)
    created_at = models.DateTimeField("作成日", auto_now=True)

    def __str__(self):
        return str(self.name)


class Allergy(models.Model):
    ingredient = models.CharField(
        "アレルギー食品", max_length=256, blank=True, null=True)
    created_at = models.DateTimeField("作成日", auto_now=True)

    def __str__(self):
        return str(self.ingredient)


class Menu(models.Model):
    name = models.CharField("表示名", max_length=256, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    price = models.PositiveIntegerField("価格", blank=True, null=True)
    img = models.ImageField("イメージ画像", upload_to="img",
                            max_length=100, blank=True, null=True)
    formatted_img = ImageSpecField(source="img",
                                   processors=[ResizeToFill(100, 100)],
                                   format="JPEG",
                                   options={"quality": 100}
                                   )
    allergies = models.ManyToManyField(Allergy, blank=True, null=True)
    chef_img = models.ImageField("シェフの顔写真", upload_to="chef_img",
                            max_length=100, blank=True, null=True)
    formatted_chef_img = ImageSpecField(source="chef_img",
                                   processors=[ResizeToFill(70, 70)],
                                   format="JPEG",
                                   options={"quality": 100}
                                   )
    comment = models.TextField("コメント", max_length=500, blank=True, null=True)
    created_at = models.DateTimeField("作成日", auto_now=True)

    def __str__(self):
        return str(self.name)


class Nomiho(models.Model):
    name = models.CharField("飲み放題プラン名", max_length=256, blank=True, null=True)
    price = models.PositiveIntegerField("価格", blank=True, null=True)
    duration = models.PositiveIntegerField("制限時間（分）", blank=True, null=True)
    comment = models.CharField("一押しポイント", max_length=256, blank=True, null=True)
    created_at = models.DateTimeField("作成日", auto_now=True)

    def __str__(self):
        return str(self.name)
