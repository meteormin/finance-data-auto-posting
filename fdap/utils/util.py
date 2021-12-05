import re
import json
import ctypes
from datetime import datetime
from typing import Dict
from configparser import ConfigParser
from fdap.definitions import CONFIG_PATH


def snake(s: str):
    """
    Is it ironic that this function is written in camel case, yet it
    converts to snake case? hmm..
    """
    underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
    underscorer2 = re.compile('([a-z0-9])([A-Z])')

    subbed = underscorer1.sub(r'\1_\2', s)
    return underscorer2.sub(r'\1_\2', subbed).lower()


def camel(s: str):
    return s.title().replace('_', '')


def make_url(host, method: str, parameters: dict = None):
    url = host + method
    count = 0
    query_str = ''
    if parameters is not None:
        for key, value in parameters.items():
            if count == 0:
                query_str = '?{0}={1}'.format(key, value)
            else:
                query_str += '&{0}={1}'.format(key, value)
            count += 1

    return url + query_str


def get_query_str_dict(url: str) -> Dict[str, str]:
    parameters = url.split('?')[1]
    parameters = parameters.split('&')

    rs_dict = {}
    for param in parameters:
        [key, value] = param.split('=')
        rs_dict[key] = value

    return rs_dict


def config_ini(name: str) -> ConfigParser:
    config_parser = ConfigParser()
    config_parser.read(CONFIG_PATH + '/{filename}.ini'.format(filename=name))
    return config_parser


def config_json(name: str) -> dict:
    with open(CONFIG_PATH + '/{filename}.json'.format(filename=name), 'r', encoding='utf-8') as f:
        return json.load(f)


def write_config_json(name, data: dict):
    with open(CONFIG_PATH + '/{filename}.json'.format(filename=name), 'w', encoding='utf-8') as f:
        return json.dump(data, f)


def object_to_json(obj: object):
    return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=2, ensure_ascii=False)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except(Exception,):
        return False


def get_quarter(date: datetime):
    if date.month < 4:
        quarter = 1
    elif date.month < 7:
        quarter = 2
    elif date.month < 10:
        quarter = 3
    elif date.month <= 12:
        quarter = 4
    else:
        quarter = 0

    return quarter


def currency_to_int(currency: str) -> int:
    numeric = currency.replace(',', '')
    if numeric.strip('-').isnumeric():
        return int(numeric)
    return 0
