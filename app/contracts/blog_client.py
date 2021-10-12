from abc import ABC, abstractmethod
from dataclasses import dataclass
from app.client.client import Client
from typing import Dict


@dataclass(frozen=False)
class BlogPostData(ABC):
    title: str
    content: str


@dataclass(frozen=True)
class BlogLoginInfo(ABC):
    pass


class BlogResource(ABC, Client):
    _resource: str
    access_token: str


class BlogPost(BlogResource):

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def write(self, data: BlogPostData):
        pass

    @abstractmethod
    def modify(self, data: BlogPostData):
        pass

    @abstractmethod
    def attach(self, filename: str, content: str):
        pass


class BlogLogin(ABC, Client):

    @abstractmethod
    def login(self, login_info: BlogLoginInfo):
        pass


class BlogEndPoint(ABC):
    _end_point: str
    _resources: Dict[type, BlogResource] = {}
    _classes: Dict[str, type] = {}

    def set_resource(self, name: type, res: BlogResource):
        self._resources[name] = res.set_host(res.get_host() + self._end_point)
        return self

    def get_resource(self, name: type):
        return self._resources[name]


class BlogClient(ABC, Client):
    _end_points: Dict[type, BlogEndPoint] = {}
    _classes: Dict[str, type] = {}

    @abstractmethod
    def login(self, obj: object):
        pass

    def set_end_point(self, name: type, end_point: BlogEndPoint):
        self._end_points[name] = end_point
        return self

    def get_end_point(self, name: type = None):
        if name is None:
            return self._end_points
        if name in self._end_points:
            return self._end_points[name]
        return None
