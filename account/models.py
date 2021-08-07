import uuid
from django.db import models
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils import timezone
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('メールアドレスは必須です。')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('rootユーザーは、is_staff=Trueである必要があります。')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('rootユーザーは、is_superuser=Trueである必要があります。')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("メールアドレス", unique=True)
    name = models.CharField("店名", max_length=256, blank=True, null=True)
    logo = models.ImageField("ロゴ", upload_to="logo",
                             max_length=50, blank=True, null=True)
    formatted_logo = ImageSpecField(source="logo",
                                    processors=[ResizeToFill(30, 30)],
                                    format="JPEG",
                                    options={"quality": 70}
                                    )
    is_staff = models.BooleanField("IAM", default=False)
    is_active = models.BooleanField("有効", default=True)
    date_joined = models.DateTimeField("登録日", default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


# for customer
class nonLoginUser(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    allowed = models.CharField(
        "アクセス制限", max_length=256, default="unknown", blank=True, null=True)
    table = models.PositiveIntegerField("テーブルの番号", blank=True, null=True)
    price = models.PositiveIntegerField(
        "お会計金額", default=0, blank=True, null=True)
    active = models.BooleanField("食事中", default=False, blank=True, null=True)
    nomiho = models.BooleanField("飲み放題中", default=False, blank=True, null=True)
    nomiho_name = models.CharField(
        "飲み放題プラン名", max_length=256, blank=True, null=True)
    nomiho_price = models.PositiveIntegerField(
        "飲み放題の合計金額", default=0, blank=True, null=True)
    created_at = models.DateTimeField("日付", auto_now=True)

    def __str__(self):
        return str(self.uuid)


class Table(models.Model):
    table = models.PositiveIntegerField(
        "テーブルの番号", default=0, blank=True, null=True)
    price = models.PositiveIntegerField(
        "テーブル毎合計", default=0, blank=True, null=True)
    active = models.BooleanField("現在", default=False, blank=True, null=True)
    created_at = models.DateTimeField("日付", auto_now=True)

    def __str__(self):
        return str(self.table)
