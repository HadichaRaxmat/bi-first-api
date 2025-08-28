from django.db import models
from core.base import BaseModel

class Result(BaseModel):
    title = models.CharField(max_length=100, verbose_name="title")
    image = models.ImageField(upload_to='results/', verbose_name="image")
    description = models.TextField(blank=True, null=True, verbose_name="description")

    class Meta:
        verbose_name = "result"
        verbose_name_plural = "results"

    def __str__(self):
        return f"{self.title} ({self.description})"