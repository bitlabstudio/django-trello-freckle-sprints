"""Views for the sprints app."""
from django.views.generic import TemplateView


class BacklogView(TemplateView):
    template_name = 'sprints/backlog_view.html'
