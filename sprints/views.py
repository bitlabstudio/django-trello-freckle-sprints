"""Views for the sprints app."""
from django.conf import settings
from django.views.generic import TemplateView

import trello_api
import freckle_api


class BacklogView(TemplateView):
    template_name = 'sprints/backlog_view.html'

    def get_context_data(self, **kwargs):
        ctx = super(BacklogView, self).get_context_data(**kwargs)

        board = self.request.GET.get('board')
        rate = int(self.request.GET.get('rate') or 0)
        list_ = None
        tr_board = None

        c = trello_api.TrelloClient(
            api_key=settings.TRELLO_DEVELOPER_KEY,
            api_secret=settings.TRELLO_DEVELOPER_SECRET,
            oauth_token=settings.TRELLO_OAUTH_TOKEN,
            oauth_secret=settings.TRELLO_OAUTH_TOKEN_SECRET,
            rate=rate,
        )

        if board:
            tr_board = c.get_board(board)
            list_ = c.get_list(tr_board, 'Backlog')

        ctx.update({
            'board': tr_board,
            'list_': list_,
        })
        return ctx


class SprintView(TemplateView):
    template_name = 'sprints/sprint_view.html'

    def get_context_data(self, **kwargs):
        ctx = super(SprintView, self).get_context_data(**kwargs)

        board = self.request.GET.get('board')
        sprint = self.request.GET.get('sprint')
        rate = int(self.request.GET.get('rate') or 0)
        list_ = None

        c = trello_api.TrelloClient(
            api_key=settings.TRELLO_DEVELOPER_KEY,
            api_secret=settings.TRELLO_DEVELOPER_SECRET,
            oauth_token=settings.TRELLO_OAUTH_TOKEN,
            oauth_secret=settings.TRELLO_OAUTH_TOKEN_SECRET,
            rate=rate,
        )

        if board and sprint:
            tr_board = c.get_board(board)
            list_ = c.get_list(tr_board, sprint)

        fr_client = freckle_api.FreckleClient(
            'bitmazk', settings.FRECKLE_API_TOKEN, rate)

        start_date = None
        if sprint:
            start_date = sprint[-10:]

        entries = fr_client.get_entries(30976, start_date)
        fr_client.enrich_trello_cards(list_, entries)

        ctx.update({
            'board': tr_board,
            'list_': list_,
        })
        return ctx
