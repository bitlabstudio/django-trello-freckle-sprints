"""Views for the sprints app."""
import re

from django.conf import settings
from django.views.generic import TemplateView

from trello import TrelloClient


class BacklogView(TemplateView):
    template_name = 'sprints/backlog_view.html'

    def get_context_data(self, **kwargs):
        ctx = super(BacklogView, self).get_context_data(**kwargs)
        trello_client = TrelloClient(
            api_key=settings.TRELLO_DEVELOPER_KEY,
            api_secret=settings.TRELLO_DEVELOPER_SECRET,
            token=settings.TRELLO_OAUTH_TOKEN,
            token_secret=settings.TRELLO_OAUTH_TOKEN_SECRET)
        board = self.request.GET.get('board')
        rate = int(self.request.GET.get('rate', 0))
        cards = None
        total_time = 0
        total_cost = 0
        if board:
            board = trello_client.get_board(board)
            lists = board.get_lists('open')
            for list_ in lists:
                if list_.name == 'Backlog':
                    cards = list_.list_cards()
                    for card in cards:
                        m = re.search(r'\((\d+)\)$', card.name)
                        if m:
                            card.estimated_time = int(m.groups()[0])
                            card.estimated_cost = \
                                card.estimated_time / 60.0 * rate
                            total_time += card.estimated_time
        if total_time and rate:
            total_cost = total_time / 60.0 * rate
        ctx.update({
            'board': board,
            'cards': cards,
            'total_time': total_time,
            'total_cost': total_cost,
        })
        return ctx
