from django.contrib import admin
from .models import Title, Header, ContactUs, Subscribe, Location, ContactNumber

admin.site.register(Title)
admin.site.register(Header)
admin.site.register(ContactNumber)
admin.site.register(Location)

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')

admin.site.register(Subscribe)