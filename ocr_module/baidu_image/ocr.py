# encoding:utf-8
import requests
from . import tokens

# 全局保存 api key 和 secret key
_API_KEY = ''
_SECRET_KEY = ''


def set_key(apikey, secret_key):
    global _API_KEY, _SECRET_KEY
    _API_KEY = apikey
    _SECRET_KEY = secret_key


def general_ocr(img_b64: bytes) -> dict:
    """
    通用文字识别
    """
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    params = {"image": img_b64}
    access_token = tokens.get_token(_API_KEY, _SECRET_KEY)
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response.json().get('error_code') is None:
        return response.json()
    else:
        raise Exception(response.json().get('error_msg'))


def accurate_ocr(img_b64: bytes) -> dict:
    """
    精确文字识别
    """
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    params = {"image": img_b64}
    access_token = tokens.get_token(_API_KEY, _SECRET_KEY)
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response.json().get('error_code') is None:
        return response.json()
    else:
        raise Exception(response.json().get('error_msg'))


def netpic_ocr(img_b64: bytes) -> dict:
    """
    网络文字识别
    """
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/webimage"

    params = {"image": img_b64}
    access_token = tokens.get_token(_API_KEY, _SECRET_KEY)
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response.json().get('error_code') is None:
        return response.json()
    else:
        raise Exception(response.json().get('error_msg'))


def number_ocr(img_b64: bytes) -> dict:
    """
    数字识别
    """
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/numbers"

    params = {"image": img_b64}
    access_token = tokens.get_token(_API_KEY, _SECRET_KEY)
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response.json().get('error_code') is None:
        return response.json()
    else:
        raise Exception(response.json().get('error_msg'))