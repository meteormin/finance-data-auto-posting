from fdap.utils.util import object_to_json
from fdap.contracts.jsonable import Jsonable
import json


class BaseData(Jsonable):

    def to_json(self) -> str:
        return object_to_json(self)


class BaseCollection(Jsonable):
    _items: list

    def count(self):
        return len(self._items)

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

    def to_dict(self):
        dict_list = []
        for item in self._items:
            dict_list.append(item.__dict__)
        return dict_list

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False, sort_keys=True)
