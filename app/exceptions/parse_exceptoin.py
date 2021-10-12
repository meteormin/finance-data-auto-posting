class ParseException(Exception):
    _code: int
    _message: str

    def __init__(self, code: int, message: str):
        self._code = code
        self._message = message

    def __str__(self):
        return "{name} - [Error: {code}] {message}".format(
            name=self.__class__.__name__,
            code=self._code,
            message=self._message
        )
