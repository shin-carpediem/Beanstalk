from django.db import models
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.utils import timezone
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, name, password, **extra_fields):
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, password, **extra_fields)

    def create_superuser(self, name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('rootユーザーは、is_staff=Trueである必要があります。')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('rootユーザーは、is_superuser=Trueである必要があります。')
        return self._create_user(name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField("店名", max_length=256, unique=True)
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

    USERNAME_FIELD = "name"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


# for customer
class nonLoginUser(models.Model):
    name = models.CharField("名前", max_length=256, blank=True, null=True)
    table = models.PositiveIntegerField("テーブルの番号", blank=True, null=True)
    session = models.ForeignKey(
        Session, blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField("日付", auto_now=True)

    class Meta:
        verbose_name = "non_login_user"
        verbose_name_plural = "non_login_users"

    def __str__(self):
        return str(self.table)
