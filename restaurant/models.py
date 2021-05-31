from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.
class Category(models.Model):
    name = models.CharField("カテゴリ", max_length=256, blank=True, null=True)
    created_at = models.DateTimeField("作成日", auto_now=True)

    def __str__(self):
        return str(self.name)


class Allergy(models.Model):
    ingredient = models.CharField("アレルギー食品", max_length=256, blank=True, null=True)
    created_at = models.DateTimeField("作成日", auto_now=True)

    def __str__(self):
        return str(self.ingredient)


class Menu(models.Model):
    name = models.CharField("表示名", max_length=256, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    price = models.PositiveIntegerField("価格", blank=True, null=True)
    img = models.ImageField("イメージ画像", upload_to="img",
                            max_length=50, blank=True, null=True)
    formatted_img = ImageSpecField(source="img",
                                   processors=[ResizeToFill(100, 100)],
                                   format="JPEG",
                                   options={"quality": 100}
                                   )
    allergies = models.ManyToManyField(Allergy, blank=True, null=True)
    created_at = models.DateTimeField("作成日", auto_now=True)

    def __str__(self):
        return str(self.name)
