from app.utils.util import object_to_json
from app.contracts.jsonable import Jsonable


class BaseData(Jsonable):

    def to_json(self) -> str:
        return object_to_json(self)
