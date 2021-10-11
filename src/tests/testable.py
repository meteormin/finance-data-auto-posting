from abc import ABC, abstractmethod
from src.utils.customlogger import CustomLogger, LoggerAdapter
from datetime import datetime
from src.contracts.jsonable import Jsonable
from src.utils.data import BaseData
import traceback
import json


class Testable(ABC):
    TAG: str = 'test'
    output_format: str = '{datetime} - {name} - {level} - {message}'
    _logger: LoggerAdapter
    _save_result: bool

    def __init__(self, save_result: bool = False):
        self._logger = CustomLogger().logger('test', self.TAG)
        self._save_result = save_result

    def run(self):
        try:
            result = self.handle()
            self._logger.debug('success')
            self._logger.debug('result:' + str(result))
            self.info(str(result))
            if self._save_result:
                self._save_json_file(result)
        except (Exception,):
            self._logger.error('fail')
            self._logger.error('ERROR:')
            self._logger.error(traceback.print_exc())
            self.error('Fail test')
            self.error(traceback.print_exc())

    def __console(self, level, msg):
        now = datetime.now()
        now.strftime('%Y-%m-%d %H:%M:%S,%f')
        print(self.output_format.format(datetime=now, name=self.TAG, level='INFO', message=msg))

    def info(self, msg: str):
        self._logger.info(msg)
        self.__console('INFO', msg)

    def debug(self, msg: str):
        self._logger.debug(msg)
        self.__console('DEBUG', msg)

    def warning(self, msg):
        self._logger.warning(msg)
        self.__console('WARNING', msg)

    def error(self, msg):
        self._logger.error(msg)
        self.__console('ERROR', msg)

    def _save_json_file(self, result):
        with open('test' + '_' + self.TAG + '.json', 'w+', encoding='utf-8') as f:
            if isinstance(result, str):
                f.write(result)
            elif isinstance(result, Jsonable):
                f.write(result.to_json())
            else:
                f.write(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))

    @abstractmethod
    def handle(self):
        pass
