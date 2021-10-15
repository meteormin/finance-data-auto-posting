from fdap.app.utils.util import object_to_json
from fdap.app.contracts.jsonable import Jsonable


class BaseData(Jsonable):

    def to_json(self) -> str:
        return object_to_json(self)


class BaseCollection(Jsonable):
    _items: list

    def push(self, item: BaseData):
        self._items.append(BaseData)
        return self

    def pop(self):
        self._items.pop()
        return self

    def first(self):
        return self.get(0)

    def last(self):
        return self.get(len(self._items) - 1)

    def get(self, key: int):
        return self._items[key]

    def all(self):
        return self._items

    def to_json(self):
        json_list = []
        for item in self._items:
            json_list.append(item.__dict__)
