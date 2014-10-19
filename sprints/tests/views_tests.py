"""Tests for the views of the sprints app."""
from django.test import TestCase, RequestFactory

from ..views import BacklogView


class BacklogViewTestCase(TestCase):
    """Tests for the ``BacklogView`` view class."""
    longMessage = True

    def test_view(self):
        req = RequestFactory().get('/')
        resp = BacklogView.as_view()(req)
        self.assertEqual(resp.status_code, 200, msg=(
            'Should be callable'))
