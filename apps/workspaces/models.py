from django.conf import settings
from django.db import models

from core.models.base import TimestampedModel, SoftDeleteQuerySet, SoftDeleteManager


# Create your models here.
class WorkspaceQuerySet(SoftDeleteQuerySet):
    def visible_to(self, user):
        if not user.is_authenticated:
            return self.none()

        return self.filter(
            memberships__user=user,
            memberships__is_active=True,
            memberships__deleted_at__isnull=True,
        ).distinct()


class WorkspaceMembershipQuerySet(SoftDeleteQuerySet):
    def enabled(self):
        return self.filter(
            is_active=True,
            deleted_at__isnull=True,
        )

    def for_user(self, user):
        return self.enabled().filter(user=user)


class Workspace(TimestampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='workspaces/', blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_workspaces')

    class Meta:
        ordering = ('name', 'created_at')
        constraints = [
            models.UniqueConstraint(
                fields=("owner", "name"),
                condition=models.Q(is_deleted=False),
                name="unique_workspace_name_per_owner",
            )
        ]

    objects = SoftDeleteManager.from_queryset(WorkspaceQuerySet)()

    def __str__(self):
        return self.name


class WorkspaceMembership(TimestampedModel):
    class Role(models.TextChoices):
        OWNER = 'owner', 'Owner'
        ADMIN = 'admin', 'Admin'
        MEMBER = 'member', 'Member'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "workspace"],
                condition=models.Q(is_deleted=False),
                name="unique_workspace_membership",
            )
        ]
        ordering = ('workspace__name', 'user__mobile')

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workspace_membership')
    role = models.CharField(choices=Role.choices, default=Role.MEMBER, max_length=20)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    objects = SoftDeleteManager.from_queryset(WorkspaceMembershipQuerySet)()

    def __str__(self):
        return f'{self.user} - {self.workspace}'
