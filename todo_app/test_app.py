import mongomock
import pymongo
import pytest
from dotenv import load_dotenv, find_dotenv

from todo_app import app
from todo_app.data.mongo_items import ItemStatus


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client


def test_index_page(client):
    # Given
    given_db_has_one_document()

    # When
    response = client.get('/')

    # Then
    assert response.status_code == 200
    assert 'This is a test title' in response.data.decode()


def given_db_has_one_document():
    client = pymongo.MongoClient('fakemongo.com')

    client['todo-app-db']['cards'].insert_one({
        "title": "This is a test title",
        "status": ItemStatus.TO_DO.value
    })
