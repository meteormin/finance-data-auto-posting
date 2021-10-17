import requests
import json
from typing import Union


class Client:
    """
    requests wrapper
    """

    def __init__(self, host: str = None):
        """

        Args:
            host(str): 요청할 웹 서버의 호스트정보(URL), ex) https://www.example.com
        """
        self._host = host
        self._response = None
        self._error = {}

    def is_success(self) -> bool:
        """
        응답의 성공여부 확인
        Returns:
            bool: 응답 상태 코드가 200번대이면 True, 아니면 False
        """
        if self._response is None:
            return False
        elif isinstance(self._response, requests.Response):
            if self._response.status_code == requests.codes.ok:
                return True
        return False

    def _set_response(self, response: requests.Response) -> Union[str, dict]:
        """
        응답 객체 결과 등록 및 에러 유무 체크
        Args:
            response(requests.Response): requests를 통해 받은 응답을 현재 wrapper에 등록하여 에러 체크 및 응답 결과를 json 혹은 text로 변환

        Returns:
            Union[str, dict]
        """
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
        """
        _set_response 메서드에서 등록된 에러를 출력
        Returns:
            dict: 'status_code': 응답 코드, 'message': 응답 메세지
        """
        return self._error

    def get_response(self) -> requests.Response:
        """
        requests 패키지에서 받은 응답 객체 가져오기

        Returns:
            requests.Response: 응답 객체 원본
        """
        return self._response

    def get_host(self) -> str:
        """
        host 가져오기 getter

        Returns:
            str: ex) https://www.example.com
        """
        return self._host

    def set_host(self, host: str):
        """

        Args:
            host(str): 호스트 정보 입력 setter

        Returns:
            Client:
        """
        self._host = host
        return self
