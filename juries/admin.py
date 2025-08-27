from django.contrib import admin
from .models import AddJury

@admin.register(AddJury)
class JuryAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')

