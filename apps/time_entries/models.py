from django.core.exceptions import ValidationError
from django.db import models
from core.models.base import TimestampedModel, SoftDeleteQuerySet, SoftDeleteManager
from apps.workspaces.models import Workspace
from django.conf import settings
from apps.projects.models import Project
from apps.tags.models import Tag
from django.utils import timezone
from datetime import timedelta


class TimeEntryQuerySet(SoftDeleteQuerySet):
    def visible_to(self, user):
        if not user.is_authenticated:
            return self.none()

        return self.filter(user=user)

    def running(self):
        return self.filter(end_time__isnull=True)


class TimeEntry(TimestampedModel):
    objects = SoftDeleteManager.from_queryset(TimeEntryQuerySet)()
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="time_entries",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="time_entries",
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="time_entries",
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="time_entries",
    )

    description = models.TextField(
        blank=True,
    )

    start_time = models.DateTimeField(
        default=timezone.now,
    )

    end_time = models.DateTimeField(
        null=True,
        blank=True,
    )

    duration = models.DurationField(
        null=True,
        blank=True,
    )

    is_billable = models.BooleanField(
        default=False,
    )

    @property
    def duration_seconds(self):
        if self.duration is None:
            return None

        return self.duration.total_seconds()

    def clean(self):
        super().clean()

        if self.project and self.project.workspace_id != self.workspace_id:
            raise ValidationError(
                "Project must belong to the same workspace."
            )

        if (
                self.end_time
                and self.start_time
                and self.end_time < self.start_time
        ):
            raise ValidationError(
                "End time must be after start time."
            )

    def save(self, *args, **kwargs):
        if self.end_time and self.start_time:
            self.duration = max(
                self.end_time - self.start_time,
                timedelta(),
            )
        else:
            self.duration = None

        super().save(*args, **kwargs)

    def stop(self, ended_at=None):
        self.end_time = ended_at or timezone.now()

        self.full_clean()
        self.save()

        return self

    def __str__(self):
        return f'{self.user} - {self.start_time}'

    class Meta:
        verbose_name_plural = "time entries"
        ordering = ("-start_time", "-created_at")
        constraints = [
            models.UniqueConstraint(
                fields=("workspace", "user"),
                condition=models.Q(
                    end_time__isnull=True,
                    is_deleted=False,
                ),
                name="unique_running_entry_per_user_workspace",
            ),
        ]
