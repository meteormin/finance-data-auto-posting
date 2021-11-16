from pandas import DataFrame
from os.path import exists
import matplotlib.pyplot as plt


class Chart:
    _df: DataFrame
    X: str = '종목명'

    def __init__(self, df: DataFrame):
        self._df = df

    def get_df(self):
        return self._df

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

    def save_img(self, file_path: str, x: str, y: str) -> bool:
        # window ver.
        plt.rc("font", family="Malgun Gothic")
        # 마이너스 숫자 설정
        plt.rc("axes", unicode_minus=False)

        ax = self._df.plot.barh(x=x, y=y)
        ax.figure.savefig(file_path)
        return exists(file_path)
