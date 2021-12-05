from django import forms
from abc import ABC, abstractmethod


class ConfigForm(forms.Form):
    @abstractmethod
    def to_dict(self) -> dict:
        pass


class KoapyForm(ConfigForm):
    kw_id = forms.CharField(label='koapy id')
    kw_pass = forms.CharField(label='koapy pass')

    def to_dict(self) -> dict:
        return {
            'account': {
                'id': self.kw_id,
                'password': self.kw_pass
            }
        }


class DataBaseForm(ConfigForm):
    db_name = forms.CharField(label='db name')
    db_id = forms.CharField(label='db id')
    db_pass = forms.CharField(label='db pass')
    dbms = 'mysql'
    host = 'localhost'

    def to_dict(self) -> dict:
        return {
            self.dbms: {
                'id': self.db_id,
                'password': self.db_pass,
                'host': self.host,
                'db': self.db_name
            }
        }


class OpenDartForm(ConfigForm):
    op_key = forms.CharField(label='open dart api key')
    op_url = forms.CharField(label='open dart url')

    def to_dict(self) -> dict:
        return {
            'api': {
                'url': self.op_url,
                'api_key': self.op_key
            }
        }


class TistoryForm(ConfigForm):
    kakao_id = forms.CharField()
    kakao_pass = forms.CharField()
    ts_url = forms.CharField()
    client_id = forms.CharField()
    client_secret = forms.CharField()
    redirect_uri = forms.CharField()
    blog_name = forms.CharField()
    driver = forms.CharField()
    confirm_btn = forms.CharField()
    kakao_login_link = forms.CharField()
    kakao_email_input = forms.CharField()
    kakao_pass_input = forms.CharField()
    kakao_login_submit = forms.CharField()

    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"

    def to_dict(self) -> dict:
        return {
            'kakao': {
                'id': self.kakao_id,
                'password': self.kakao_pass
            },
            'api': {
                'url': self.ts_url,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'redirect_uri': self.redirect_uri,
                'response_type': 'code',
                'state': self.blog_name,
                'blog_name': self.blog_name,
                'user_agent': self.USER_AGENT,
            },
            'webdriver': {
                'driver_name': self.driver,
                'confirm_btn': self.confirm_btn,
                'kakao_login_link': self.kakao_login_link,
                'kakao_email_input': self.kakao_email_input,
                'kakao_pass_input': self.kakao_pass_input,
                'kakao_login_submit': self.kakao_login_submit
            }
        }


def get_form(module: str, data) -> ConfigForm:
    config_dict = {
        'koapy': KoapyForm,
        'opendart': OpenDartForm,
        'database': DataBaseForm,
        'tistory': TistoryForm
    }

    return config_dict[module](data)
