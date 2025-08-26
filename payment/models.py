from django.db import models
from core.base import BaseModel
from competition.models import Application
from django.utils import timezone


class Payment(BaseModel):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="payments")
    payment_id = models.CharField(max_length=100, unique=True, verbose_name=_("payment ID"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("price"))
    date_time = models.DateTimeField(default=timezone.now, verbose_name=_("date time"))

    def __str__(self):
        return f"Payment {self.payment_id} - {self.application}"