"""
Helper method to fetch data from the Trello API.

See https://trello.com/docs/index.html

"""
import json
import re

import requests
from requests_oauthlib import OAuth1


class TrelloClient(object):
    """Base class for Trello API access."""
    def __init__(self, api_key, api_secret, oauth_token, oauth_secret, rate):
        self.oauth = OAuth1(
            client_key=api_key,
            client_secret=api_secret,
            resource_owner_key=oauth_token,
            resource_owner_secret=oauth_secret)
        self.api_key = api_key
        self.api_secret = api_secret
        self.resource_owner_key = oauth_token
        self.resource_owner_secret = oauth_secret
        self.rate = rate

    def fetch_json(self, uri_path, http_method='GET', headers=None,
                   query_params=None, post_args=None):
        """Fetch some JSON from Trello."""
        # explicit values here to avoid mutable default values
        if headers is None:
            headers = {}
        if query_params is None:
            query_params = {}
        if post_args is None:
            post_args = {}

        # set content type and accept headers to handle JSON
        if http_method in ("POST", "PUT", "DELETE"):
            headers['Content-Type'] = 'application/json; charset=utf-8'
        headers['Accept'] = 'application/json'

        # construct the full URL without query parameters
        if uri_path[0] == '/':
            uri_path = uri_path[1:]
        url = 'https://api.trello.com/1/%s' % uri_path

        # perform the HTTP requests, if possible uses OAuth authentication
        response = requests.request(
            http_method, url, params=query_params, headers=headers,
            data=json.dumps(post_args), auth=self.oauth)

        if response.status_code != 200:
            raise Exception(
                "Trello API Response is not 200: %s" % (response.text))

        return response.json()

    def get_board(self, board_id):
        """Gets all important data for a board."""
        return self.fetch_json(
            'boards/{0}'.format(board_id),
            query_params={
                'lists': 'open',
                'cards': 'open',
                'card_checklists': 'all',
            }
        )

    def get_list(self, board, list_name):
        """
        Returns a dict with the list of the given name.

        Also attaches all cards belonging to that list to the dict.

        :param board: A board as returned by ``get_board()``
        :param list_name: String representing a list name.

        """
        result = None
        for list_ in board['lists']:
            if list_['name'] == list_name:
                result = list_
                result['time_estimated_total'] = 0
                result['cost_estimated_total'] = 0
                break
        list_cards = []
        for card in board['cards']:
            if card['idList'] == result['id']:
                self.enrich_card(result, card)
                list_cards.append(card)
        result['cards'] = list_cards
        return result

    def get_time_from_name(self, name):
        """
        Extracts the time (if given) from a name string.

        :param name: String representing the name of a checklist item.
        :returns: 0 if no time was estimated or an integer representing the
          minutes.

        """
        m = re.search(r'\((\d+)\)$', name)
        if not m:
            return 0
        try:
            return int(m.groups()[0])
        except TypeError:
            return 0

    def enrich_card(self, list_, card):
        """
        Iterates through the checklists of the card and adds estimated times.

        :param list_: The list of the given card. Needed to increase the list
          total time and cost.
        :param card: The card to be enriched.

        """
        time_estimated = 0
        for checklist in card['checklists']:
            if checklist['name'] == 'Buffer':
                continue
            for item in checklist['checkItems']:
                minutes = self.get_time_from_name(item['name'])
                time_estimated += minutes
        card['time_estimated'] = time_estimated
        cost_estimated = time_estimated / 60.0 * self.rate
        card['cost_estimated'] = cost_estimated
        list_['time_estimated_total'] += time_estimated
        list_['cost_estimated_total'] += cost_estimated
