import json
from dataclasses import dataclass
from typing import List
from fdap.app.utils.data import BaseData


class Data(BaseData):
    def map(self, data: dict):
        attrs = self.__dict__
        for k, v in data.items():
            if k in self.__dict__.keys():
                self.__setattr__(k, v)
        return self

    def map_list(self, data_list):
        results = []
        for data in data_list:
            results.append(self.__class__().map(data))

        return results


@dataclass
class CorpCode(Data):
    corp_code: str = None
    corp_name: str = None
    stock_code: str = None
    modify_date: str = None

    def map(self, data: dict) -> __name__:
        return super().map(data)

    def map_list(self, data_list) -> List[__name__]:
        return super().map_list(data_list)


@dataclass
class Acnt(Data):
    corp_code: str = None
    ord: str = None
    rcept_no: str = None
    bsns_year: str = None
    stock_code: str = None
    reprt_code: str = None
    account_nm: str = None
    fs_div: str = None
    fs_nm: str = None
    sj_div: str = None
    sj_nm: str = None
    thstrm_nm: str = None
    thstrm_dt: str = None
    thstrm_amount: str = None
    thstrm_add_amount: str = None
    frmtrm_nm: str = None
    frmtrm_dt: str = None
    frmtrm_amount: str = None
    frmtrm_add_amount: str = None
    bfefrmtrm_nm: str = None
    bfefrmtrm_dt: str = None
    bfefrmtrm_amount: str = None
    ord: str = None

    def map(self, data: dict) -> __name__:
        return super().map(data)

    def map_list(self, data_list) -> List[__name__]:
        return super().map_list(data_list)


class AcntCollection(Data):
    _items: List[Acnt]

    def __init__(self, acnt_list: List[Acnt] = None):
        if acnt_list is None:
            acnt_list = []
        self._items = acnt_list

    def push(self, acnt: Acnt):
        self._items.append(acnt)
        return self

    def pop(self):
        self._items.pop()
        return self

    def first(self):
        return self.get(0)

    def last(self):
        return self.get(len(self._items) - 1)

    def get(self, key: int):
        return self._items[key]

    def all(self):
        return self._items

    def get_by_account_nm(self, account_nm: str, fs_div: str = 'CFS') -> Acnt:
        for item in self._items:
            if fs_div == item.fs_div:
                if account_nm == item.account_nm:
                    return item

    def to_json(self):
        json_list = []
        for item in self._items:
            json_list.append(item.__dict__)

        return json.dumps(json_list, indent=2, ensure_ascii=False, sort_keys=True)

    def map(self, data: List[Acnt]):
        self._items = data
        return self
