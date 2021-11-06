from abc import ABC, abstractmethod
from fdap.utils.data import BaseData
from typing import Union, Dict

"""
Abstract Repositories
"""


class Repository(ABC):

    @abstractmethod
    def all(self):
        pass

    @abstractmethod
    def create(self, data: BaseData):
        pass

    @abstractmethod
    def find(self, identifier: Union[str, int]):
        pass

    @abstractmethod
    def find_by_attribute(self, attr: Dict[str, any]):
        pass

    @abstractmethod
    def update(self, identifier: Union[str, int], data: BaseData):
        pass

    @abstractmethod
    def delete(self, identifier: Union[str, int]):
        pass


class PostsRepository(Repository, ABC):
    def last(self):
        pass


class UploadedRepository(Repository, ABC):
    pass


class LinkedPostRepository(Repository, ABC):
    pass
