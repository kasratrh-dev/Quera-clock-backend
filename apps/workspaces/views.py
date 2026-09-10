from email import message

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import TemplateView, FormView
from django.contrib import messages

from apps.clients.models import Client
from apps.projects.models import Project
from apps.tags.models import Tag
from apps.time_entries.models import TimeEntry
from apps.workspaces.models import Workspace
from apps.contact_notes.forms import ContactNoteForm


class LandingView(TemplateView):
    template_name = "pages/landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["workspace_count"] = Workspace.objects.count()
        context["project_count"] = Project.objects.count()

        return context


class StatusView(TemplateView):
    template_name = "pages/status.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["workspace_count"] = Workspace.objects.count()
        context["client_count"] = Client.objects.count()
        context["project_count"] = Project.objects.count()
        context["tag_count"] = Tag.objects.count()
        context["time_entry_count"] = TimeEntry.objects.count()
        context["running_timer_count"] = TimeEntry.objects.running().count()

        return context


class AboutView(FormView):
    template_name = "pages/about.html"
    form_class = ContactNoteForm
    success_url = "/"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your message has been sent successfully.")
        return super().form_valid(form)


class DashboardPreviewView(LoginRequiredMixin, TemplateView):
    template_name = "pages/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["workspaces"] = (
            Workspace.objects
            .visible_to(self.request.user)
            .annotate(membership_count=Count("memberships"))
        )

        user_entries = TimeEntry.objects.visible_to(self.request.user)

        context["running_timer_count"] = user_entries.running().count()

        context["recent_entries"] = (
            user_entries
            .select_related("project", "workspace")
            .order_by("-created_at")[:5]
        )

        return context
