from django.db import models
from core.base import BaseModel
from home.models import Title


class Expert(BaseModel):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='experts/', null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.full_name or "Expert"


class ExpertsSocialLink(BaseModel):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=50, verbose_name="Платформа")  # Например: Facebook, Instagram
    url = models.URLField(verbose_name="Ссылка")  # Ссылка на профиль
    icon = models.ImageField(upload_to='social_icons/', null=True, blank=True, verbose_name="Иконка")  # PNG или SVG

    class Meta:
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"

    def __str__(self):
        return f"{self.platform} ({self.expert.full_name})"
