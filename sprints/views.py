"""Views for the sprints app."""
import re
import datetime

from django.conf import settings
from django.views.generic import TemplateView

from freckle import Freckle
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


class SprintView(TemplateView):
    template_name = 'sprints/sprint_view.html'

    def get_context_data(self, **kwargs):
        ctx = super(SprintView, self).get_context_data(**kwargs)
        trello_client = TrelloClient(
            api_key=settings.TRELLO_DEVELOPER_KEY,
            api_secret=settings.TRELLO_DEVELOPER_SECRET,
            token=settings.TRELLO_OAUTH_TOKEN,
            token_secret=settings.TRELLO_OAUTH_TOKEN_SECRET)
        entries = []
        board = self.request.GET.get('board')
        sprint = self.request.GET.get('sprint')
        sprint_list = None
        start_date = None
        if sprint:
            start_date = sprint.replace('Sprint-', '')
            start_date = datetime.datetime.strptime(
                start_date, '%Y-%m-%d').date()
        project = self.request.GET.get('project')
        rate = int(self.request.GET.get('rate', 0))
        cards = None
        total_time = 0
        total_cost = 0
        total_actual_time = 0
        total_actual_cost = 0

        if project and start_date:
            freckle_client = Freckle(
                account=settings.FRECKLE_ACCOUNT_NAME,
                token=settings.FRECKLE_API_TOKEN)
            entries = freckle_client.get_entries(
                projects=[project, ],
                date_from=start_date,)

        if board:
            board = trello_client.get_board(board)
            lists = board.get_lists('open')
            for list_ in lists:
                if list_.name == sprint:
                    sprint_list = list_
                    cards = list_.list_cards()
                    for card in cards:
                        m = re.search(r'\((\d+)\)$', card.name)
                        card.fetch(eager=False)
                        if m:
                            card.estimated_time = int(m.groups()[0])
                            card.estimated_cost = \
                                card.estimated_time / 60.0 * rate
                            total_time += card.estimated_time
                        time_booked = 0
                        for entry in entries:
                            if 'c%d' % card.short_id in entry['description']:
                                time_booked += entry['minutes']
                        card.actual_time = time_booked
                        total_actual_time += time_booked
                        card.actual_cost = time_booked / 60.0 * rate

        if total_time and rate:
            total_cost = total_time / 60.0 * rate
            total_actual_cost = total_actual_time / 60.0 * rate

        ctx.update({
            'entries': entries,
            'board': board,
            'sprint_list': sprint_list,
            'cards': cards,
            'total_time': total_time,
            'total_cost': total_cost,
            'total_actual_time': total_actual_time,
            'total_actual_cost': total_actual_cost,
        })
        return ctx
