class Config:
    DATABASE: str = 'database'
    KOAPY: str = 'koapy'
    LOGGER: str = 'logger'
    OPENDART: str = 'opendart'
    TISTORY: str = 'tistory'

    @classmethod
    def list(cls):
        return [
            cls.DATABASE,
            cls.KOAPY,
            cls.LOGGER,
            cls.OPENDART,
            cls.TISTORY
        ]