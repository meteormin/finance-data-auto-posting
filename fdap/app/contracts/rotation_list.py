from abc import ABC, abstractmethod


class RotationList(ABC):

    @abstractmethod
    def get_items(self):
        pass

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def prev(self):
        pass

    @abstractmethod
    def current(self):
        pass

    def rules(self):
        pass
