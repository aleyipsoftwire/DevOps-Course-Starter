import os

import requests

TRELLO_API_HOST = 'https://api.trello.com/1'
TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_API_TOKEN = os.environ.get('TRELLO_API_TOKEN')
TRELLO_BOARD_ID = os.environ.get('TRELLO_BOARD_ID')

TRELLO_TODO_LIST_ID = os.environ.get('TRELLO_TODO_LIST_ID')
TRELLO_DONE_LIST_ID = os.environ.get('TRELLO_DONE_LIST_ID')


def get_board():
    url = "{url}/boards/{id}/lists".format(
        url=TRELLO_API_HOST, id=TRELLO_BOARD_ID
    )

    headers = {"Accept": "application/json"}

    query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_API_TOKEN,
        'cards': 'open',
        'fields': 'id,name,cards',
        'card_fields': 'id,name'
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query
    )

    cards = []
    for trello_list in response.json():
        for card in trello_list['cards']:
            if trello_list['id'] == TRELLO_DONE_LIST_ID:
                status = 'Done'
            else:
                status = 'To do'

            cards.append({
                'id': card['id'],
                'title': card['name'],
                'status': status
            })

    return cards


def add_item(title):
    url = "{url}/cards".format(url=TRELLO_API_HOST)

    headers = {"Accept": "application/json"}

    query = {
        'idList': TRELLO_TODO_LIST_ID,
        'key': TRELLO_API_KEY,
        'token': TRELLO_API_TOKEN,
        'name': title
    }

    response = requests.request(
        "POST",
        url,
        headers=headers,
        params=query
    )
