import subprocess
from os.path import exists
from fdap.app.kiwoom.koapy_wrapper import KoapyWrapper
from pyhocon import ConfigFactory, HOCONConverter
from typing import List
from fdap.app.kiwoom.basic_info import BasicInfo
from fdap.utils.util import config_json
from fdap.definitions import APP_PATH
from fdap.app.contracts.service import Service


class KiwoomService(Service):
    _koapy_wrapper: KoapyWrapper = None

    def __init__(self, _id: str = None, password: str = None):
        super().__init__()

        if _id is None or password is None:
            config = config_json('koapy')
            _id = config['account']['id']
            password = config['account']['password']

        conf = ConfigFactory.parse_file(APP_PATH + '/kiwoom/config.conf')
        current_id = conf.get('koapy.backend.kiwoom_open_api_plus.credential.user_id')
        if exists('./koapy.conf'):
            current_id = ConfigFactory.parse_file('./koapy.conf').get(
                'koapy.backend.kiwoom_open_api_plus.credential.user_id')

        if current_id != _id:
            self._logger.debug('setting koapy login info')
            conf.put('koapy.backend.kiwoom_open_api_plus.credential.user_id', _id)
            conf.put('koapy.backend.kiwoom_open_api_plus.credential.user_password', password)
            new = HOCONConverter.convert(conf, "hocon")

            with open('./koapy.conf', 'w+') as f:
                f.write(new)

        conda = subprocess.run(['conda.bat', 'activate', 'x86'])
        self._logger.debug(conda.stdout)

        koapy = subprocess.run(['koapy', 'update', 'openapi'])
        self._logger.debug(koapy.stdout)

        self._koapy_wrapper = KoapyWrapper()
        self._logger.info('init:' + __name__)

    def get_sector_list(self):
        return self._koapy_wrapper.get_sector_list()

    def get_stock_list_by_sector(self, sector: str, market_code: str = '0') -> List[BasicInfo]:
        stock_info = self._koapy_wrapper.get_stock_info_by_sector_as_list(sector, market_code)
        rs_list = []
        for info in stock_info:
            basic = self._koapy_wrapper.get_stock_basic_info_as_dict(info.code)
            rs_list.append(basic)

        return rs_list

    def get_stock(self, stock_code):
        return self._koapy_wrapper.get_stock_basic_info_as_dict(stock_code)
