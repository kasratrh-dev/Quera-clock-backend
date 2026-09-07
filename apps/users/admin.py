from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['mobile', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'is_superuser']
    search_fields = ['mobile', 'email', 'first_name', 'last_name']
    ordering = ['mobile']
    readonly_fields = ['date_joined', 'last_login']

    fieldsets = (
        (None, {
            'fields': ('mobile', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'birth_date', 'description', 'profile_picture')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('date_joined', 'last_login')
        })
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("mobile", "password1", "password2"),
            },
        ),
    )