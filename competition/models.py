from django.db import models
from core.base import BaseModel
from home.models import Title


class Competition(BaseModel):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='competition_images')
