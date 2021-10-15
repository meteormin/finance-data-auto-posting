from prototype.handler import Handler


class Infographic(Handler):
    TAG: str = 'infographic'

    def handle(self):
        from prototype.refine import Refine
        from fdap.app.infographic import make_dataframe
        import dataframe_image as dfi
        from fdap.definitions import ROOT_DIR
        import matplotlib.pyplot as plt

        refine_data = Refine(self._save_result).handle()
        print(refine_data.to_dict())
        df = make_dataframe(refine_data)
        dfi.export(df, ROOT_DIR + '/../prototype/results/infographic-table.png')
        # window ver.
        plt.rc("font", family="Malgun Gothic")
        # 마이너스 숫자 설정
        plt.rc("axes", unicode_minus=False)
        ax = df.plot.barh(x='stock_name', y='market_cap')
        ax.figure.savefig(ROOT_DIR + '/../prototype/results/infographic-chart.png')

        return 'success?'
