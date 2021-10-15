from pandas import DataFrame
from fdap.app.contracts.convertible import TableData
from typing import Union


def make_dataframe(data: TableData) -> Union[DataFrame, None]:
    if isinstance(data.to_dict(), list):
        data_frame = DataFrame.from_records(data.to_dict())
    elif isinstance(data.to_dict(), dict):
        data_frame = DataFrame.from_records([data.to_dict()])
    else:
        return None

    before_sort = data_frame
    start = False
    for attr, priority in data.sort_attr().items():
        before_sort = before_sort.sort_values(attr, ascending=priority)
        if start:
            before_sort['rank'] += before_sort.index
        else:
            before_sort['rank'] = before_sort.index
            start = True

    after_sort = before_sort[[
        'rank',
        'stock_code',
        'stock_name',
        'market_cap',
        'deficit_count',
        'per',
        'pbr',
        'roe',
        'flow_rate',
        'debt_rate'
    ]]

    return after_sort
