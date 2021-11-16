from fdap.app.contracts.rotation_list import RotationList
from fdap.app.contracts.repositories import PostsRepository
import collections


class RotationSector(RotationList):
    _repo: PostsRepository
    _items: collections.deque
    _rule: dict
    _except: list = [
        '001',
        '002',
        '003',
        '004',
        '603',
        '604',
        '605'
    ]

    def __init__(self, repo: PostsRepository, items: list, rules: dict = None):
        self._repo = repo
        self._items = self._except_codes(items)
        self._rule = rules

    def _except_codes(self, items: list):
        excepted_items = []
        for item in items:
            if item['code'] not in self._except:
                excepted_items.append(item)
        return collections.deque(excepted_items)

    def get_items(self):
        return self._items

    def next(self):
        self._items.rotate(-1)
        return self.current()

    def current(self):
        return self._items[0]

    def prev(self):
        self._items.rotate(1)
        return self.current()

    def rules(self):
        return self._rule

    def get_sector(self, year: str, report_code: str):
        sectors = self._repo.find_by_attribute({
            'post_year': year,
            'report_code': report_code
        })

        cnt = 0
        while cnt < len(self._items):
            not_equals = 0
            for sector in sectors:
                if sector.post_sector == self.current()['code']:
                    self.next()
                    break
                else:
                    not_equals += 1
            if not_equals == len(sectors):
                break
            cnt += 1

        return self.current()
