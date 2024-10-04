import os
from enum import Enum

import pymongo
from bson import ObjectId


class ItemStatus(Enum):
    TO_DO = 'TO_DO'
    DONE = 'DONE'


class MongoItem:
    def __init__(self, id: ObjectId, title, status: ItemStatus):
        ObjectId()

        self.id = id
        self.title = title
        self.status = status

    @classmethod
    def from_mongo_document(self, document):
        return self(
            document['_id'],
            document['title'],
            ItemStatus(document['status'])
        )


def get_mongo_items():
    client = pymongo.MongoClient(os.getenv('MONGODB_PRIMARY_CONNECTION_STRING'))

    collection = client['todo-app-db']['cards']

    cards = []
    for document in collection.find():
        card = MongoItem.from_mongo_document(document)
        cards.append(card)

    return cards


def add_mongo_item(title: str):
    client = pymongo.MongoClient(os.getenv('MONGODB_PRIMARY_CONNECTION_STRING'))

    cards = client['todo-app-db']['cards']

    post = {
        "title": title,
        "status": ItemStatus.TO_DO.value
    }

    cards.insert_one(post)


def update_mongo_item_status(item_id: str, status: ItemStatus):
    client = pymongo.MongoClient(os.getenv('MONGODB_PRIMARY_CONNECTION_STRING'))

    cards = client['todo-app-db']['cards']

    cards.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": {
            "status": status.value
        }},
    )
