"""
Helper method to fetch data from the Freckle API.

See http://developer.letsfreckle.com

"""
import json
import re

import requests


class FreckleClient(object):
    """Base class for Freckle API access."""
    def __init__(self, account_name, api_token, rate):
        self.account_name = account_name
        self.api_token = api_token
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
        query_params['token'] = self.api_token

        # construct the full URL without query parameters
        if uri_path[0] == '/':
            uri_path = uri_path[1:]
        url = 'https://{0}.letsfreckle.com/api/{1}'.format(
            self.account_name, uri_path)

        # perform the HTTP requests, if possible uses OAuth authentication
        response = requests.request(
            http_method, url, params=query_params, headers=headers,
            data=json.dumps(post_args))

        if response.status_code != 200:
            raise Exception(
                "Freckle API Response is not 200: %s" % (response.text))

        return response.json()

    def get_entries(self, project, start_date, end_date):
        """
        Returns the entries for the given project and time frame.

        :param project: The project ID.
        :param start_date: String representing the start date (YYYY-MM-DD).
        :param end_date: String representing the end date (YYYY-MM-DD).

        """
        result = {
            'entries': [],
            'cards': {},
            'has_non_cards': False,
            'total_time': 0,
        }
        result['entries'] = self.fetch_json(
            'entries',
            query_params={
                'per_page': 1000,
                'search[from]': start_date,
                'search[to]': end_date,
                'search[projects]': '{0}'.format(project),
                'search[billable]': 'true',
            }
        )

        total_time = 0
        for entry in result['entries']:
            m = re.search(r'c(\d+)', entry['entry']['description'])
            if m:
                card_short_id = int(m.groups()[0])
                if card_short_id not in result['cards']:
                    result['cards'][card_short_id] = {
                        'minutes': 0,
                        'shortId': card_short_id,
                    }
                result['cards'][card_short_id]['minutes'] += \
                    entry['entry']['minutes']
                entry['entry']['has_card'] = True
            else:
                entry['entry']['has_card'] = False
                entry['entry']['cost'] = \
                    entry['entry']['minutes'] / 60.0 * self.rate
                result['has_non_cards'] = True
            total_time += entry['entry']['minutes']
        result['total_time'] = total_time
        return result

    def enrich_trello_cards(self, list_, entries):
        """
        Iterates through entries and adds actual times to the Trello list.

        :param list_: The list as returned by ``TrelloClient.get_list()``.
        :param entries: The Freckle entries as returned by ``get_entries()``.

        """
        time_actual = 0
        cost_actual = 0
        for card in list_['cards']:
            for entry in entries:
                entry = entry['entry']
                if 'c%d' % card['idShort'] in entry['description']:
                    card['time_actual'] = entry['minutes']
                    card_cost_actual = entry['minutes'] / 60.0 * 120
                    card['cost_actual'] = card_cost_actual
                    cost_actual += card_cost_actual
                    time_actual += entry['minutes']
        list_['time_actual_total'] = time_actual
        list_['cost_actual_total'] = cost_actual
