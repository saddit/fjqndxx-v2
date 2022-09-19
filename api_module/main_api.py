import base64
import importlib
import logging
import time
from datetime import datetime

import requests
import urllib3
from exception import KnownException
from ocr_module import util as ocrutil

# 处理https警告
urllib3.disable_warnings()


CRYPT_NAME = "sm4"
CRYPT_MODE = "ecb"
MAX_TRY = 5

encryptor = importlib.import_module(
    f"crypt_module.{CRYPT_NAME}.{CRYPT_NAME}_{CRYPT_MODE}")

sess = requests.session()
sess.verify = False
sess.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Host": "m.fjcyl.com",
    "Referer": "https://m.fjcyl.com/login"
})


def init_proxy():
    logging.info("正在尝试使用代理IP")
    module = importlib.import_module("proxy_module.proxy_fetcher")
    proxy = module.ProxyFecher()
    while not proxy.empty():
        ip = f"http://{proxy.random_pop()}"
        try:
            logging.info(f"正在测试 {ip}")
            sess.get("https://m.fjcyl.com/",
                     proxies={'https': ip}, timeout=8)

            logging.info(f"测试成功，使用{ip}代理请求")
            sess.proxies = {"https": ip}
        except BaseException as e:
            logging.info(f"{ip} 不可用, {e}")
    raise KnownException("找不到可用代理IP")


def get_validate_code() -> str:
    max_try = 5
    has_try = 0
    while has_try < max_try:
        try:
            resp = sess.get(url=f"https://m.fjcyl.com/validateCode", timeout=10)
            # noinspection PyUnresolvedReferences
            res = ocrutil.img_ocr(base64.b64encode(resp.content))
            logging.info(f'获取验证码成功: {res}')
            return res
        except Exception as e:
            logging.warning(f'获取验证码失败，原因:{e}')
            logging.warning(f'正在重试, 次数:{has_try}')
            has_try += 1
            time.sleep(1)

    if has_try == max_try:
        raise KnownException("验证码解析失败,请尝试更换方式或发issue寻求帮助")


def post_study_record():
    has_try = 0
    errmsg = ""
    while has_try < MAX_TRY:
        try:
            resp = sess.post(url="https://m.fjcyl.com/studyRecord", timeout=12)
            if resp.json().get('success'):
                logging.info("学习成功！")
                return
            else:
                has_try += 1
                errmsg = resp.json()['errmsg']
                logging.error(f"学习失败，正在重试{has_try}, {resp.text}")
        except requests.ReadTimeout:
            has_try += 1
            errmsg = "timeout"
            logging.error(f"学习失败，正在重试{has_try},超时")

    raise KnownException(f"学习失败,{errmsg}")


def post_login(username: str, pwd: str, pub_key: str, code: str):
    post_dict = {
        'userName': encryptor.encrypt(username, pub_key),
        'pwd': encryptor.encrypt(pwd, pub_key),
        'validateCode': encryptor.encrypt(code, pub_key)
    }

    resp = sess.post(url="https://m.fjcyl.com/mobileNologin",
                     data=post_dict, timeout=5)

    if resp.status_code == requests.codes['ok']:
        if resp.json().get('success'):
            logging.info(username[-4:] + ' login ' + resp.json().get('errmsg'))
        else:
            raise ConnectionError(resp.json().get('errmsg'))
    else:
        raise KnownException(
            f'官方服务器发生异常,错误代码:{resp.status_code},信息:{resp.text}')
