from django.contrib import admin
from .models import Children

@admin.register(Children)
class ChildrenAdmin(admin.ModelAdmin):
    list_display = ("get_first_name", 'first_name', 'last_name', 'birth_date', 'study_place', 'type_of_kind')

    def get_first_name(self, obj):
        return obj.parent.first_name  # теперь корректно берём поле из родителя

    get_first_name.short_description = "Parent First Name"


