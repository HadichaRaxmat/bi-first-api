from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Children(models.Model):
    class KindChoices(models.TextChoices):
        SON = "son", _("Son")
        DAUGHTER = "daughter", _("Daughter")

    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="children", verbose_name=_("Parent"))
    image = models.ImageField(blank=True, null=True, verbose_name=_("Child Image"))
    first_name = models.CharField(max_length=255, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, verbose_name=_("Last Name"))
    father_name = models.CharField(max_length=255, verbose_name=_("Father Name"))
    birth_date = models.DateField(verbose_name=_("Birth Date"))
    study_place = models.CharField(max_length=255, verbose_name=_("Study Place"))
    type_of_kind = models.CharField(max_length=10, choices=KindChoices.choices, verbose_name=_("Type of Kind"))

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_type_of_kind_display()})"

