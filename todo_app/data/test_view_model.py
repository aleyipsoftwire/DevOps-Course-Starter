from todo_app.data.trello_items import Item
from todo_app.data.models import ViewModel


def test_should_return_correct_done_list():
    # Given
    items = [
        Item("1", "item1", "Done"),
        Item("2", "item2", "To do"),
        Item("3", "item3", "Done"),
    ]

    # When
    view_model = ViewModel(items)

    # Then
    assert view_model.done_items[0].id == "1"
    assert view_model.done_items[1].id == "3"
