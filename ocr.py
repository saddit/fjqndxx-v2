# encoding:utf-8
import json
import logging
import requests

""" 
ocr使用百度的接口，如果需要更换请保持general_ocr函数名、参数不变，
并修改main.py中get_validate_code的相关语句
"""

# 加载 api key 和 secret key
_API_KEY = ""
_SECRET_KEY = ""
try:
    with open('config123.json', 'r') as config:
        jsons = json.loads(config.read())
        _API_KEY = jsons.get('ocr').get('ak')
        _SECRET_KEY = jsons.get('ocr').get('sk')
except FileNotFoundError as e:
    logging.warning(e.filename + ":" + '读取config配置文件出错，请确保ocr所需key已经正确输入')


def set_key(apikey, secret_key):
    global _API_KEY, _SECRET_KEY
    _API_KEY = apikey
    _SECRET_KEY = secret_key


def _get_token() -> str:
    global _API_KEY, _SECRET_KEY
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token' \
           f'?grant_type=client_credentials&client_id={_API_KEY}&client_secret={_SECRET_KEY}'
    response = requests.get(host)
    if response.ok:
        return response.json().get('access_token')
    else:
        logging.warning(response.json().get('error_description'))
        return ""


def general_ocr(img_b64: bytes) -> dict:
    """
    通用文字识别
    """
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"

    params = {"image": img_b64}
    access_token = _get_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response.ok:
        return response.json()
    else:
        logging.warning(response.json().get('error-msg'))
