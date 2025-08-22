from django.contrib import admin
from .models import Competition, Application, CompetitionSubscriber

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'age', 'start_date', "end_date")



@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_first_name', 'competition', 'get_children', 'payment_method')

    def get_email(self, obj):
        return obj.parent.email

    get_email.admin_order_field = 'parent__email'
    get_email.short_description = 'Email'

    def get_first_name(self, obj):
        return obj.parent.first_name  # теперь корректно берём поле из родителя

    get_first_name.short_description = "First Name"

    def get_children(self, obj):
        return ", ".join([str(child) for child in obj.children.all()])  # использует __str__ модели Children

    get_children.short_description = "Children"

@admin.register(CompetitionSubscriber)
class CompetitionSubscriberAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscriber', 'competition')