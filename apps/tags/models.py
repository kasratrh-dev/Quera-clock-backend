from django.db import models
from core.models.base import TimestampedModel, SoftDeleteManager,SoftDeleteQuerySet
from apps.workspaces.models import Workspace



class TagQuerySet(SoftDeleteQuerySet):
    def visible_to(self, user):
        if not user.is_authenticated:
            return self.none()

        return self.filter(
            workspace__memberships__user=user,
            workspace__memberships__is_active=True,
            workspace__memberships__deleted_at__isnull=True,
        ).distinct()



class Tag(TimestampedModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=120)
    color = models.CharField(max_length=20, default='#64748b')

    class Meta:
        ordering = ('name',)

        constraints = [
            models.UniqueConstraint(fields=('workspace', 'name'), condition=models.Q(is_deleted=False),
                                    name='unique_tag_name_per_workspace'),


        ]

    objects = SoftDeleteManager.from_queryset(TagQuerySet)()

    def __str__(self):
        return self.name




