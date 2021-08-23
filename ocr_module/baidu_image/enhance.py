import logging
from PIL import Image
import requests
import json
import base64
from . import tokens

# 加载 api key 和 secret key
_API_KEY = ''
_SECRET_KEY = ''
try:
    with open('config.json', 'r') as config:
        jsons = json.loads(config.read())
        _API_KEY = jsons.get('enhance').get('ak')
        _SECRET_KEY = jsons.get('enhance').get('sk')
except FileNotFoundError as e:
    logging.warning(e.filename + ":" + '读取config配置文件出错，请确保enhance所需key已经正确输入')


def definition_enhance(img_b64: bytes) -> str:
    """
    清晰度增强
    """
    request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/image_definition_enhance"

    params = {"image": img_b64}
    access_token = tokens.get_token(_API_KEY, _SECRET_KEY)
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response.json().get('error_code') is None:
        return response.json()['image']
    else:
        raise Exception("definition fail:"+response.json().get('error_msg'))


def decode_image_byte(func: function, *args, **kwargs):
    return base64.decodebytes(func(args,kwargs).encode("utf-8"))



def quality_enhance(img_b64: bytes) -> str:
    """
    无损放大两倍
    """
    request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/image_quality_enhance"

    params = {"image": img_b64}
    access_token = tokens.get_token(_API_KEY, _SECRET_KEY)
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response.json().get('error_code') is None:
        return response.json()['image']
    else:
        raise Exception("quality fail:" + response.json().get('error_msg'))


def convert_img(img: Image, threshold) -> Image:
    """
    灰度处理+二值化
    :param img: PIL.Image
    :param threshold: 一般是 150
    :return: PIL.Image
    """
    img = img.convert("L")  # 处理灰度
    pixels = img.load()
    for x in range(img.width):
        for y in range(img.height):
            if pixels[x, y] > threshold:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
    return img