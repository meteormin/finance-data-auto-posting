from pandas import DataFrame
from fdap.app.contracts.convertible import TableData
from typing import Union
import dataframe_image as dfi
from os.path import exists


class Table:
    _data: TableData

    def __init__(self, data: TableData):
        self._data = data

    def get_data(self):
        return self._data

    @staticmethod
    def get_ko_col_names() -> dict:
        return {
            'rank': '순위',
            'stock_code': '종목코드',
            'stock_name': '종목명',
            'current_price': '현재가',
            'market_cap': '시가총액',
            'deficit_count': '적자횟수',
            'per': 'PER',
            'pbr': 'PBR',
            'roe': 'ROE',
            'flow_rate': '유동비율',
            'debt_rate': '부채비율'
        }

    def sort_dataframe(self, df: DataFrame, col: list) -> Union[DataFrame, None]:
        before_sort = df
        data = self._data

        start = False
        for attr, priority in data.sort_attr().items():
            before_sort = before_sort.sort_values(attr, ascending=priority)
            if start:
                before_sort['rank'] += before_sort.index
            else:
                before_sort['rank'] = before_sort.index
                start = True

        before_sort.sort_values('rank', ascending=True)
        after_sort = before_sort[col]

        return after_sort

    def make_dataframe(self) -> Union[DataFrame, None]:
        data = self._data

        if isinstance(data.to_dict(), list):
            data_frame = DataFrame.from_records(data.to_dict())
        elif isinstance(data.to_dict(), dict):
            data_frame = DataFrame.from_records([data.to_dict()])
        else:
            return None
        df = self.sort_dataframe(data_frame, list(self.get_ko_col_names().keys()))
        df = df.rename(columns=self.get_ko_col_names())

        return df

    def save_img(self, file_path: str) -> bool:
        df = self.make_dataframe()
        df_styled = df.style.hide_index()
        df_styled = df_styled.set_properties(**{'text-align': 'center'})
        dfi.export(df_styled, file_path)

        return exists(file_path)
