from todo_app.data.mongo_items import ItemStatus


class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def done_items(self):
        return [item for item in self._items if item.status == ItemStatus.DONE]

    @property
    def todo_items(self):
        return [item for item in self._items if item.status == ItemStatus.TO_DO]
