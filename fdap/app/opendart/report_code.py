from enum import Enum, unique


@unique
class ReportCode(Enum):
    Q1 = '11013'
    Q2 = '11012'
    Q3 = '11014'
    Q4 = '11011'

    @classmethod
    def get_by_str(cls, q: str) -> __name__:
        for k, v in cls.__members__.items():
            if q == v.value:
                return v

    @classmethod
    def get_by_index(cls, i: int) -> __name__:
        for k, v in enumerate(cls.__members__.values()):
            if k + 1 == i:
                return v

    @classmethod
    def get_index(cls, q: str) -> int:
        for idx, v in enumerate(cls.__members__.values()):
            if v.value == q:
                return idx + 1

    @classmethod
    def sub(cls, quarter: str, sub_num: int) -> __name__:
        has_attr = False
        for q in cls.__members__.values():
            if quarter == q.value:
                has_attr = True

        if has_attr is False:
            raise AttributeError(quarter + ' has not attribute')

        if sub_num >= 4:
            remainder = sub_num % 4
            return cls.sub(quarter, remainder)

        member_list = list(cls.__members__)
        rs = 0
        for idx, member in enumerate(member_list):
            if cls.__members__[member].value == quarter:
                if idx == 0:
                    if sub_num != 0:
                        tmp = sub_num - 1
                        rs = (len(cls.__members__) - 1) - tmp
                    else:
                        rs = idx
                else:
                    rs = idx - sub_num
                print(rs)
                return cls.__members__[member_list[rs]]
