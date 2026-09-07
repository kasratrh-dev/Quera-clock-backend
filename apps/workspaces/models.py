from django.conf import settings
from django.db import models

from core.models import TimestampedModel


# Create your models here.


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


    def __str__(self):
        return f'{self.user} - {self.workspace}'