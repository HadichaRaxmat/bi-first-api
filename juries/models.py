from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from core.base import BaseModel

class AddJuries(BaseModel):
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name=_("Email"))
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name=_("Phone"))
    image = models.ImageField(blank=True, null=True, verbose_name=_("user_Image"))
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Last Name"))
    father_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Father Name"))
    birth_date = models.DateField(blank=True, null=True, verbose_name=_("Birth Date"))
    work_place = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Work place"))
    academic_degree = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Academic Degree"))
    profession = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Profession"))
    login = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Login"))
    password = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Password"))

    class Meta:
        verbose_name = _("Jury")
        verbose_name_plural = _("Juries")

    def __str__(self):
        full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
        return full_name if full_name else "Jury"
