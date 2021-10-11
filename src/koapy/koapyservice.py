from os.path import exists
from src.koapy.koapywrapper import KoapyWrapper
from pyhocon import ConfigFactory, HOCONConverter
import subprocess
from src.utils.customlogger import CustomLogger
from typing import List
from src.koapy.basicinfo import BasicInfo
from src.utils.util import config_ini


class KoapyService:

    def __init__(self, _id: str = None, password: str = None):
        self._logger = CustomLogger.logger('automatic-posting', __name__)

        if _id is None or password is None:
            config = config_ini('koapy')
            _id = config['account']['id']
            password = config['account']['password']

        conf = ConfigFactory.parse_file('modules/koapy/config.conf')
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
            conda = subprocess.run(['conda', 'activate', 'x86'])
            self._logger.debug(conda.stdout)

            koapy = subprocess.run(['koapy', 'update', 'openapi'])
            self._logger.debug(koapy.stdout)

        self._koapy_wrapper = KoapyWrapper()
        self._logger.info('init:' + __name__)

    def get_sector_list(self):
        return self._koapy_wrapper.get_sector_list()

    def get_stock_list_by_sector(self, sector: str) -> List[BasicInfo]:
        stock_info = self._koapy_wrapper.get_stock_info_by_sector_as_list(sector)
        rs_list = []
        for info in stock_info:
            basic = self._koapy_wrapper.get_stock_basic_info_as_dict(info.code)
            rs_list.append(basic)

        return rs_list
