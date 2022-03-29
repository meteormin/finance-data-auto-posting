from pandas import DataFrame
from fdap.contracts.convertible import TableData
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

    def sort_dataframe(self, df: DataFrame, col: list) -> DataFrame:
        before_sort = df
        data = self._data

        if df.empty:
            return df

        for attr, priority in data.sort_attr().items():
            if attr in before_sort:
                before_sort = before_sort.sort_values(attr, ascending=priority)
        #     if 'rank' in before_sort:
        #         before_sort['rank'] += before_sort.index
        #     else:
        #         before_sort['rank'] = before_sort.index
        #
        # after_sort = before_sort.sort_values('rank', ascending=True)
        after_sort = before_sort
        return after_sort[col]

    def make_dataframe(self, stock_cond: int = 1, cnt: int = 10) -> Union[DataFrame, None]:
        data = self._data

        if isinstance(data.to_dict(), list):
            data_frame = DataFrame.from_records(data.to_dict())
        elif isinstance(data.to_dict(), dict):
            data_frame = DataFrame.from_records([data.to_dict()])
        else:
            return None

        df = self.sort_dataframe(data_frame, list(self.get_ko_col_names().keys()))
        if df.empty:
            return None

        df = df.rename(columns=self.get_ko_col_names())

        if stock_cond == 1:
            df = df.head(cnt)
        elif stock_cond == 2:
            df = df.tail(cnt)
        else:
            df = df.head(cnt)

        return df

    def save_img(self, file_path: str) -> bool:
        df = self.make_dataframe()
        df_styled = df.style.hide_index()
        df_styled = df_styled.set_properties(**{'text-align': 'center'})
        dfi.export(df_styled, file_path)

        return exists(file_path)
