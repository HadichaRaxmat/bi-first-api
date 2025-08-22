from django.db import models
from core.base import BaseModel
from home.models import Title
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone


class Competition(BaseModel):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="competitions", verbose_name=_("title"))
    image = models.ImageField(upload_to="competition_images/", blank=True, null=True, verbose_name=_("Images"))
    description = models.TextField(verbose_name=_("description"))
    age = models.CharField(max_length=20, verbose_name=_("age"))
    start_date = models.DateField(default=timezone.now, verbose_name=_("start date"))
    end_date = models.DateField(verbose_name=_("end date"), null=True, blank=True)

    class Meta:
        verbose_name = _("competition")
        verbose_name_plural = _("competitions")
        ordering = ["-end_date"]

    def __str__(self):
        return str(self.title)



class Application(BaseModel):
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="applications")
    children = models.ManyToManyField("children.Children", related_name="applications")
    physical_certificate = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, choices=[("payme", "Payme"), ("click", "Click")], null=True, blank=True)

    def __str__(self):
        return f"{self.parent} → {self.competition}"




class CompetitionSubscriber(BaseModel):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="competition_subscriptions")
    competition = models.ForeignKey("Competition", on_delete=models.CASCADE, related_name="subscribers")

    class Meta:
        unique_together = ('subscriber', 'competition')
        verbose_name = _("Competition Subscriber")
        verbose_name_plural = _("Competition Subscribers")

    def __str__(self):
        return f"{self.subscriber} → {self.competition}"
