from fdap.contracts.logging import Logging
from fdap.contracts.core import Container as Parent
from fdap.contracts.service import Service
import traceback
from datetime import datetime


class Container(Logging, Parent):
    _TAG: str = 'Core'
    output_format: str = '{datetime} - {name} - {level} - {message}'
    _service: Service

    def __init__(self, instance: Service):
        super().__init__()
        self._logger.info('application start')
        self._service = instance

    def run(self, action: str, **kwargs):
        self._logger.info('run service...')
        try:
            callback = getattr(self._service.__class__, action)
            response = callback(self._service, **kwargs)
            self._logger.info('result: ' + str(response))
            self.__console('info', 'result: ' + str(response))
            self._logger.info('application end')
            return 0
        except BaseException as e:
            self._logger.error('Error:' + str(e))
            self._logger.error(traceback.format_exc())
            return 1

    def __console(self, level, msg):
        now = datetime.now()
        now.strftime('%Y-%m-%d %H:%M:%S,%f')
        print(self.output_format.format(datetime=now, name=self._TAG, level=level, message=msg))
