from django.contrib import admin
from django.contrib.auth.admin import (
    GroupAdmin as BaseGroupAdmin,
    UserAdmin as BaseUserAdmin,
)
from django.contrib.auth.models import Group

from unfold.admin import ModelAdmin
from unfold.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)

from apps.users.models import User

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
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
