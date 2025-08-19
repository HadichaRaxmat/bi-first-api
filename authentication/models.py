from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        if not email and not phone:
            raise ValueError("User must have either email or phone")

        extra_fields.setdefault("is_active", True)

        # Убираем email/phone из extra_fields, если вдруг передали
        extra_fields.pop("email", None)
        extra_fields.pop("phone", None)

        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email=email, phone=phone, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name=_("Email"))
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name=_("Phone"))
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Last Name"))
    father_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Father Name"))
    birth_date = models.DateField(blank=True, null=True, verbose_name=_("Birth Date"))

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"   # для суперюзеров и джанго
    REQUIRED_FIELDS = []       # username убираем

    def __str__(self):
        return self.first_name or self.email
