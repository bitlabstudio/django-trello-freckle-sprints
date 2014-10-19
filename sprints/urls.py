"""URLs for the sprints app."""
from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^backlog/$',
        views.BacklogView.as_view(),
        name='sprints_backlog'),
)
