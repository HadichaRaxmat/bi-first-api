from django.contrib import admin
from .models import Title, Header, ContactUs, Subscribe, Location, ContactNumber, SocialMedia, Result

admin.site.register(Title)
admin.site.register(Header)
admin.site.register(ContactNumber)
admin.site.register(Location)
admin.site.register(Result)

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')

admin.site.register(Subscribe)

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image', 'url')