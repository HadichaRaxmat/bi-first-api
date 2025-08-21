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




class ContactUs(BaseModel):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, verbose_name=_('title'))
    description = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('description'))

    class Meta:
        verbose_name = _('Contact us')
        verbose_name_plural = _('Contact us')

    def __str__(self):
        return f'{self.title}'

class Subscribe(BaseModel):
    email = models.EmailField(blank=True, null=True, verbose_name=_('email'))

    class Meta:
        verbose_name = _('Subscriber')
        verbose_name_plural = _('subscribers')

    def __str__(self):
        return f'{self.email}'


class Location(BaseModel):
    title = models.ForeignKey(ContactUs, on_delete=models.CASCADE, verbose_name=_('location'))
    image = models.ImageField(upload_to="location", blank=True, verbose_name=_('image'))

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    def __str__(self):
        return f'{self.title}'

class ContactNumber(BaseModel):
    contact_us = models.ForeignKey(ContactUs, on_delete=models.CASCADE, verbose_name=_('numbers'))
    number = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('number'))
    image = models.ImageField(upload_to="number", blank=True, verbose_name=_('image'))

    class Meta:
        verbose_name = _('Contact number')
        verbose_name_plural = _('Contact numbers')

    def __str__(self):
        return f'{self.contact_us, self.number}'


class SocialMedia(BaseModel):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, verbose_name=_('title'))
    image = models.ImageField(upload_to="social-media", blank=True, verbose_name=_('image'))
    url = models.URLField(blank=True, null=True, verbose_name=_('url'))

    def __str__(self):
        return f'{self.title}'