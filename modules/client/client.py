import requests
from configparser import ConfigParser
import os
import json


class Client:
    """ just Http request client
    Attributes:
        _host (str): my lumen server IP
        _client_id (int): Oauth2.0 client_id
        _client_secret (str): Oauth2.0 client_secret
        _token (str): access_token
    """

    def __init__(self):
        config = ConfigParser()
        config.read(os.path.dirname(
            os.path.realpath(__file__)) + '/client.ini')

        self._host = config.get('access_info', 'client_host')
        self._client_id = config.get('access_info', 'client_id')
        self._client_secret = config.get('access_info', 'client_secret')
        self._token = None

    def getToken(self):
        """get access token

        Returns:
            str: access token
        """
        if (self._token == None):
            end_point = '/oauth/token'
            body = {
                "grant_type": "client_credentials",
                "client_id": self._client_id,
                "client_secret": self._client_secret
            }

            res = requests.post(self._host + end_point, data=body).json()
            self._token = res['access_token']
            return self._token
        else:
            return self._token

    def getStocks(self):
        """get stocks information
        Returns:
            dict:
        """
        end_point = '/api/stocks'

        res = requests.get(self._host + end_point)

        if (res.status_code == requests.codes.ok):
            return res.json()
        else:
            return res.text

    def getSectors(self, market=''):
        """get sectors information
        Args:
            market (str): market code
        Returns:
            dict:
        """

        end_point = '/api/sectors/' + market
        res = requests.get(
            self._host + end_point, headers={'Authorization': 'Bearer ' + self.getToken()})
        if (res.status_code == requests.codes.ok):
            return res.json()
        else:
            return res.text

    def postThemeList(self, themes):
        end_point = '/api/themes'
        res = requests.post(self._host + end_point, json=themes,
                            headers={'Authorization': 'Bearer ' + self.getToken()})
        if (res.status_code == requests.codes.ok):
            return res.json()
        else:
            return res.text

    def postStocks(self, method, stocks):
        """ send to stocks information
        Args:
            stocks (list): list of StockInfo dict
        Returns:
            dict:
        """
        end_point = '/api/stocks/' + method

        res = requests.post(self._host + end_point, json=stocks,
                            headers={'Authorization': 'Bearer ' + self.getToken()})

        if (res.status_code == requests.codes.ok):
            return res.json()
        else:
            return res.text

    def postSectorList(self, sectors, market = 'kospi'):
        end_point = '/api/sectors/kospi'
        res = requests.post(self._host + end_point, json=sectors,
                            headers={'Authorization': 'Bearer ' + self.getToken()})
        if (res.status_code == requests.codes.ok):
            return res.json()
        else:
            return res.text