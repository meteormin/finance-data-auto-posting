from fdap.utils.util import config_json


class Config:
    DATABASE: dict = config_json('database')
    KOAPY: dict = config_json('koapy')
    LOGGER: dict = config_json('logger')
    OPENDART: dict = config_json('opendart')
    TISTORY: dict = config_json('tistory')

    @classmethod
    def list(cls):
        return [
            cls.DATABASE,
            cls.KOAPY,
            cls.LOGGER,
            cls.OPENDART,
            cls.TISTORY
        ]
