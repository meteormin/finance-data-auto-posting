import requests
import zipfile
import io
import xmltodict
from src.client.client import Client
from typing import Dict, Union
from src.utils.util import make_url


class OpenDartClient(Client):

    def __init__(self, host: str, api_key: str):
        super().__init__(host)
        self._api_key = api_key

    def get_corp_codes(self) -> Union[Dict[str, str], None]:
        end_point = '/api/corpCode.xml'
        url = make_url(host=self.get_host(), method=end_point, parameters={'crtfc_key': self._api_key})
        self._response = requests.get(url)
        res = self._response.content
        if res is not None:
            with zipfile.ZipFile(io.BytesIO(res)) as zip_ref:
                zip_ref.extractall()

            with open('CORPCODE.xml', 'r', encoding='utf-8') as f:
                corp_code_xml = f.read()
            return xmltodict.parse(corp_code_xml).get('result').get('list')
        return None

    def get_single(self, corp_code: str, year: str, report_code: str):
        end_point = '/api/fnlttSinglAcnt.json'
        url = make_url(self.get_host(), end_point, {
            'crtfc_key': self._api_key,
            'corp_code': corp_code,
            'bsns_year': year,
            'reprt_code': report_code
        })
        print(url)
        res = requests.get(url)

        return self._set_response(res)

    def get_multi(self, corp_codes: list, year: str, report_code: str):
        end_point = '/api/fnlttMultiAcnt.json'
        corp_codes = ','.join(corp_codes)

        url = make_url(self.get_host(), end_point, {
            'crtfc_key': self._api_key,
            'corp_code': corp_codes,
            'bsns_year': year,
            'reprt_code': report_code
        })

        res = requests.get(url)

        return self._set_response(res)
