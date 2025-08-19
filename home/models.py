from django.db import models
from core.base import BaseModel
from django.utils.translation import gettext_lazy as _

class Title(BaseModel):
    name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('name'))
    name2 = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('name2'))

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Title')
        verbose_name_plural = _('Titles')


class Header(BaseModel):
    title = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('title'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))
    bg_image = models.ImageField(upload_to="header", blank=True, verbose_name=_('background image'))

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Header')
        verbose_name_plural = _('Headers')

