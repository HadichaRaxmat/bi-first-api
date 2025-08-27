from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from competition.models import Competition
from .models import User, EmailVerification

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("id", "email", "phone", "first_name", "last_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")

    # убираем username, добавляем email/phone
    fieldsets = (
        (None, {"fields": ("email", "phone", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "father_name", "birth_date")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "phone", "password1", "password2", "is_staff", "is_active")}
        ),
    )
    search_fields = ("email", "phone", "first_name", "last_name")
    ordering = ("email",)  # ⚡️ исправлено — больше не username


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    model = EmailVerification
    list_display = ("id", "user", "code", "expires_at")


