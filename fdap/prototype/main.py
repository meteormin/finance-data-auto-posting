import json

from fdap.prototype.handler import Handler
from fdap.app.tistory.tistory_client import PostData


class Main(Handler):
    TAG: str = 'main'

    def handle(self):
        from fdap.prototype.tistory import Tistory
        import os
        from fdap.definitions import ROOT_DIR

        # infographic = Infographic().make('013', '2021', ReportCode.Q1)
        with open(os.path.join(ROOT_DIR, 'results/infographic.json'), 'r', encoding='utf-8') as f:
            infographic = json.load(f)

        tistory = Tistory(save_result=self._save_result)
        tistory.login()
        tistory.client.apis().post().access_token = tistory.client.access_token

        rs_list = []
        table = infographic['table']
        with open(table, 'rb') as f:
            f_name = os.path.basename(table)
            contents = f.read()
            rs = tistory.client.apis().post().attach(f_name, contents)
            self._logger.debug(str(rs))
            rs_list.append(self.make_img_tag(rs['tistory']['url'], f_name) + ('<p>&nbsp;</p>' * 3))

        for chart in infographic['chart']:
            with open(chart, 'rb') as f:
                f_name = os.path.basename(chart)
                contents = f.read()
                rs = tistory.client.apis().post().attach(f_name, contents)
                self._logger.debug(str(rs))
                rs_list.append(self.make_img_tag(rs['tistory']['url'], f_name) + ('<p>&nbsp;</p>' * 3))

        post = PostData(
            title=self.test_subject('013', '2021', 1),
            content=' '.join(rs_list),
            visibility=0
        )

        return tistory.client.apis().post().write(post)

    @staticmethod
    def test_subject(sector: str, year: str, q: int):
        return f"{sector}: {year}년 {q}분기(TEST)"

    @staticmethod
    def make_img_tag(url: str, h_text: str):
        return f"<p>{h_text}</p> <img src={url}>"
