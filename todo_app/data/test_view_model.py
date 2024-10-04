from bson import ObjectId

from todo_app.data.models import ViewModel

from todo_app.data.mongo_items import MongoItem, ItemStatus


def test_should_return_correct_done_list():
    # Given
    id1 = ObjectId()
    id2 = ObjectId()
    id3 = ObjectId()
    items = [
        MongoItem(id1, "item1", ItemStatus.DONE),
        MongoItem(id2, "item2", ItemStatus.TO_DO),
        MongoItem(id3, "item3", ItemStatus.DONE),
    ]

    # When
    view_model = ViewModel(items)

    # Then
    assert view_model.done_items[0].id == id1
    assert view_model.done_items[1].id == id3


def test_should_return_correct_todo_list():
    # Given
    id1 = ObjectId()
    id2 = ObjectId()
    id3 = ObjectId()
    items = [
        MongoItem(id1, "item1", ItemStatus.DONE),
        MongoItem(id2, "item2", ItemStatus.TO_DO),
        MongoItem(id3, "item3", ItemStatus.DONE),
    ]

    # When
    view_model = ViewModel(items)

    # Then
    assert view_model.todo_items[0].id == id2
