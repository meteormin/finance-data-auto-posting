from modules.client.client import Client
from bs4 import BeautifulSoup
from selenium import webdriver

class TistoryClient(Client):

    def __init__(self, host: str, api_key: str):
        super().__init__(host=host)
        self._api_key = api_key

    @staticmethod
    def login(_id: str, password: str):
        browser = webdriver.Chrome()



