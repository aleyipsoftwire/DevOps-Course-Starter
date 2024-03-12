import os

import requests

TRELLO_API_HOST = 'https://api.trello.com/1'


class Item:
    def __init__(self, id, title, status='To Do'):
        self.id = id
        self.title = title
        self.status = status

    @classmethod
    def from_trello_card(cls, card, list_id):
        if list_id == os.getenv('TRELLO_DONE_LIST_ID'):
            status = 'Done'
        else:
            status = 'To do'

        return cls(card['id'], card['name'], status)


def get_trello_board():
    url = "{url}/boards/{id}/lists".format(
        url=TRELLO_API_HOST, id=os.getenv('TRELLO_BOARD_ID')
    )

    headers = {"Accept": "application/json"}

    query = {
        'key': os.getenv('TRELLO_API_KEY'),
        'token': os.getenv('TRELLO_API_TOKEN'),
        'cards': 'open',
        'fields': 'id,name,cards',
        'card_fields': 'id,name'
    }

    response = requests.get(
        url,
        headers=headers,
        params=query
    )

    cards = []
    for trello_list in response.json():
        for card in trello_list['cards']:
            card = Item.from_trello_card(card, trello_list['id'])
            cards.append(card)

    return cards


def add_trello_item(title):
    url = "{url}/cards".format(url=TRELLO_API_HOST)

    headers = {"Accept": "application/json"}

    query = {
        'idList': os.getenv('TRELLO_TODO_LIST_ID'),
        'key': os.getenv('TRELLO_API_KEY'),
        'token': os.getenv('TRELLO_API_TOKEN'),
        'name': title
    }

    requests.post(
        url,
        headers=headers,
        params=query
    )


def update_trello_item_status(item_id, status):
    url = "{url}/cards/{id}".format(url=TRELLO_API_HOST, id=item_id)

    headers = {"Accept": "application/json"}

    if status == 'done':
        id_list = os.getenv('TRELLO_DONE_LIST_ID')
    else:
        id_list = os.getenv('TRELLO_TODO_LIST_ID')

    query = {
        'idList': id_list,
        'key': os.getenv('TRELLO_API_KEY'),
        'token': os.getenv('TRELLO_API_TOKEN'),
    }

    requests.put(
        url,
        headers=headers,
        params=query
    )
