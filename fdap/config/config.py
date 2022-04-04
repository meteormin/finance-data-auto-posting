from fdap.utils.util import config_json


class Config:
    DATABASE: dict = config_json('database')
    KOAPY: dict = config_json('koapy')
    LOGGER: dict = config_json('logger')
    OPENDART: dict = config_json('opendart')
    TISTORY: dict = config_json('tistory')

    @classmethod
    def all(cls) -> dict:
        return {
            'database': cls.DATABASE,
            'koapy': cls.KOAPY,
            'logger': cls.LOGGER,
            'opendart': cls.OPENDART,
            'tistory': cls.TISTORY
        }

    @classmethod
    def get(cls, name: str) -> dict:
        return cls.all()[name]
