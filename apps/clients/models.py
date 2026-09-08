from django.db import models

from core.models.base import TimestampedModel, SoftDeleteManager, SoftDeleteQuerySet
from apps.workspaces.models import Workspace


class ClientQuerySet(SoftDeleteQuerySet):
    def visible_to(self, user):
        if not user.is_authenticated:
            return self.none()

        return self.filter(
            workspace__memberships__user=user,
            workspace__memberships__is_active=True,
            workspace__memberships__deleted_at__isnull=True,
        ).distinct()


class Client(TimestampedModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    notes = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='clients/', blank=True, null=True)

    class Meta:
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(fields=('workspace', 'name')
                                    , condition=models.Q(is_deleted=False),
                                    name='unique_client_name_per_workspace'),

        ]

    objects = SoftDeleteManager.from_queryset(ClientQuerySet)()

    def __str__(self):
        return self.name
