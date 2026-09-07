from core.admins.base import SoftDeleteAdmin
from django.contrib import admin
from .models import Workspace, WorkspaceMembership


# Register your models here.

class WorkspaceMembershipInline(admin.TabularInline):
    model = WorkspaceMembership
    extra = 0
    fields = (
        "is_deleted",
        "deleted_at",
        "user",
        "role",
        'is_active',
    )
    readonly_fields = (
        "joined_at",
    )


@admin.register(Workspace)
class WorkspaceAdmin(SoftDeleteAdmin):
    list_display = ('name', 'owner', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'owner__mobile')
    ordering = ('name',)

    inlines = [
        WorkspaceMembershipInline,
    ]
    fieldsets = (
        (None, {
            'fields': ('is_deleted', 'deleted_at', 'name', 'description', 'thumbnail', 'owner')
        }),

    )


@admin.register(WorkspaceMembership)
class WorkspaceMembershipAdmin(SoftDeleteAdmin):
    list_display = ('workspace', 'user', 'role', 'is_active', 'joined_at')
    list_filter = ('role', 'is_active', 'joined_at')
    search_fields = ('workspace__name', 'user__mobile')
