from django.core.exceptions import ValidationError
from django.db import models
from core.models.base import TimestampedModel, SoftDeleteQuerySet, SoftDeleteManager
from apps.workspaces.models import Workspace
from apps.clients.models import Client


class ProjectQuerySet(SoftDeleteQuerySet):
    def visible_to(self, user):
        if not user.is_authenticated:
            return self.none()

        return self.filter(
            workspace__memberships__user=user,
            workspace__memberships__is_active=True,
            workspace__memberships__deleted_at__isnull=True,
        ).distinct()

    def not_archived(self):
        return self.filter(is_archived=False)


class Project(TimestampedModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='projects')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=20, default='#2563eb')
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='projects/', blank=True, null=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(fields=['workspace', 'name'], condition=models.Q(is_deleted=False),
                                    name='unique_project_name_per_workspace'),
        ]

    def clean(self):
        if self.client and self.client.workspace != self.workspace:
            raise ValidationError(
                "Client must belong to the same workspace."
            )

    objects = SoftDeleteManager.from_queryset(ProjectQuerySet)()

    def __str__(self):
        return self.name
