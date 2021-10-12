from app.contracts.logging import Logging
from app.exceptions.parse_exceptoin import ParseException


class Service(Logging):

    def __init__(self):
        super().__init__()

    def throw(self, code: int, message: str):
        raise ParseException(code, message)
