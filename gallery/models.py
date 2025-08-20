from core.base import BaseModel
from django.db import models
from home.models import Title


class Gallery(BaseModel):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='galleries', verbose_name='Gallery Title')
    image = models.ImageField(upload_to='galleries', verbose_name='Gallery Image')
    description = models.TextField(verbose_name='Gallery Description')

    def __str__(self):
        return self.title