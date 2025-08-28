from django.db import models
from core.base import BaseModel
from home.models import Title

class About(BaseModel):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    title2 = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return str(self.title)


class Founders(BaseModel):
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name='founders')
    image = models.ImageField(upload_to='founders/')
    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name