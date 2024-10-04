import mongomock
import pymongo
import pytest
from dotenv import load_dotenv, find_dotenv

from todo_app.data.mongo_items import ItemStatus, get_mongo_items, add_mongo_item, update_mongo_item_status


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        yield None


def test_get_mongo_item(client):
    # Given
    given_db_has_one_document()

    # When
    items = get_mongo_items()

    # Then
    assert len(items) == 1
    assert items[0].title == 'This is a test title'
    assert items[0].status == ItemStatus.TO_DO


def test_add_mongo_item(client):
    # When
    add_mongo_item("This is another test title")

    # Then
    items = get_mongo_items()
    assert len(items) == 1
    assert items[0].title == 'This is another test title'
    assert items[0].status == ItemStatus.TO_DO


def test_update_mongo_item(client):
    # Given
    inserted_id = given_db_has_one_document().inserted_id

    # When
    update_mongo_item_status(inserted_id, ItemStatus.DONE)

    # Then
    items = get_mongo_items()
    assert len(items) == 1
    assert items[0].status == ItemStatus.DONE


def given_db_has_one_document():
    client = pymongo.MongoClient('fakemongo.com')

    return client['todo-app-db']['cards'].insert_one({
        "title": "This is a test title",
        "status": ItemStatus.TO_DO.value
    })
