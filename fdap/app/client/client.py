import requests
import json
from typing import Union


class Client:

    def __init__(self, host: str = None):
        self._host = host
        self._response = None
        self._error = {}

    def is_success(self) -> bool:
        if self._response is None:
            return False
        elif isinstance(self._response, requests.Response):
            if self._response.status_code == requests.codes.ok:
                return True
        return False

    def _set_response(self, response: requests.Response) -> Union[str, dict]:
        self._response = response
        if self.is_success():
            try:
                return self._response.json()
            except json.decoder.JSONDecodeError:
                return self._response.text
        else:
            self._error['status_code'] = self._response.status_code
            self._error['message'] = self._response.text
            return self._response.text

    def get_error(self) -> dict:
        return self._error

    def get_response(self) -> requests.Response:
        return self._response

    def get_host(self) -> str:
        return self._host

    def set_host(self, host: str):
        self._host = host
        return self
