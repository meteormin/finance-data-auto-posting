from abc import ABC, abstractmethod


class BlogClient(ABC):

    @abstractmethod
    def login(self, obj: object):
        pass


class BlogPost(ABC):

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def write(self, obj: object):
        pass

    @abstractmethod
    def modify(self, obj: object):
        pass

    @abstractmethod
    def attach(self, filename: str, content: str):
        pass

