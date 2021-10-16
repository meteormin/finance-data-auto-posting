from abc import ABC, abstractmethod


class TableData(ABC):

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def sort_attr(self) -> dict:
        pass