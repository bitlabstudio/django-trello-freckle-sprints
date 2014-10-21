"""Tests for the views of the sprints app."""
from django.test import TestCase, RequestFactory

from mock import MagicMock

from ..views import BacklogView, TrelloClient


class BacklogViewTestCase(TestCase):
    """Tests for the ``BacklogView`` view class."""
    longMessage = True

    def setUp(self):
        super(BacklogViewTestCase, self).setUp()
        self.mock_board = MagicMock()

        mock_list = MagicMock()
        mock_list.name = 'Foobar'
        self.mock_backlog = MagicMock()
        self.mock_backlog.name = 'Backlog'
        self.mock_lists = [mock_list, self.mock_backlog]
        mock_card1 = MagicMock()
        mock_card1.id = 1
        mock_card1.name = 'Foobar'
        mock_card2 = MagicMock()
        mock_card2.id = 2
        mock_card2.name = 'Something (5)'
        mock_card3 = MagicMock()
        mock_card3.id = 3
        mock_card3.name = 'Something else (120)'

        self.mock_backlog.list_cards.return_value = [
            mock_card1, mock_card2, mock_card3]
        TrelloClient.get_board = MagicMock(return_value=self.mock_board)
        self.mock_board.get_lists.return_value = self.mock_lists

    def test_view(self):
        req = RequestFactory().get('/')
        resp = BacklogView.as_view()(req)
        self.assertEqual(resp.status_code, 200, msg=('Should be callable'))

        req = RequestFactory().get('/?board=foo&rate=100')
        resp = BacklogView.as_view()(req)
        self.assertEqual(resp.status_code, 200, msg=('Should be callable'))
        self.assertEqual(resp.context_data['total_time'], 125, msg=(
            'Should iterate through all cards and add up the estimated time'))
