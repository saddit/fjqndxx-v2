import base64
import json
import logging
import requests
import ocr

from requests import cookies
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

"""
脚本识别验证码使用的是百度的api，使用前请先申请百度ocr的key！或者更改ocr.py中的代码来使用你所知道的api
运行方法：
    1. 直接运行main.py
        将config.json.bak更名为config.json, 填写config数据为你自己的数据，然后直接运行即可
    2. 通过GitHubAction等自动化工具
        不运行此脚本，运行workflow.py, 以GithubAction为例，你需要添加五个secrets，分别为
        username, pwd, pub_key, ocr_api_key, ocr_secret_key
        并在run.yml中按此顺序定义输入流, 按顺序！
"""

def init_logger():
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format="[%(levelname)s]:%(message)s")


def get_cookie() -> cookies:
    resp = requests.get(url="http://m.fjcyl.com")
    return resp.cookies


def get_validate_code(cookie) -> str:
    resp = requests.get(url="http://m.fjcyl.com/validateCode?0.123123&width=58&height=19&num=4",
                        cookies=cookie)
    res = ocr.general_ocr(base64.b64encode(resp.content))

    # 如果使用了其他api，以下内容都应进行修改
    if res.__contains__('error_msg'):
        logging.warning('get validate code - ' + res['error_msg'])
    else:
        logging.info('get validate code success')

        return res['words_result'][0]['words']


def post_study_record(cookie):
    resp = requests.post(url="http://m.fjcyl.com/studyRecord",
                         cookies=cookie)
    if resp.json().get('success'):
        logging.info("study success recorded")
    else:
        logging.warning("study record failed")


def rsa_encrypt(public_key, src):
    public_key = '-----BEGIN PUBLIC KEY-----\n' + public_key + '\n-----END PUBLIC KEY-----'
    rsa_key = RSA.importKey(public_key)
    cipher = PKCS1_v1_5.new(rsa_key)
    return str(base64.b64encode(cipher.encrypt(src.encode('utf-8'))), 'utf-8')


def post_login(username: str, pwd: str, validate_code, pub_key, cookie):
    post_dict = {
        'userName': rsa_encrypt(pub_key, username),
        'pwd': rsa_encrypt(pub_key, pwd),
        'validateCode': rsa_encrypt(pub_key, validate_code)
    }

    resp = requests.post(url="http://m.fjcyl.com/mobileNologin",
                         data=post_dict,
                         cookies=cookie)

    logging.info('login ' + resp.json().get('errmsg'))


def run(use_config: bool):
    logging.info("auto-study is Running")
    # get default config
    if use_config:
        with open('config.json', 'r') as config:
            jsons = json.loads(config.read())
            username = jsons.get('username')
            pwd = jsons.get('pwd')
            pub_key = jsons.get('rsaKey').get('public')
    else:
        username = input()
        pwd = input()
        pub_key = input()
        ocr.set_key(apikey=input(), secret_key=input())

    # get cookie / session id
    cookie = get_cookie()
    if cookie is not None:
        logging.info("get cookie success")
    else:
        logging.warning("get cookie failed")

    # get validate code
    code = get_validate_code(cookie)

    # do login
    post_login(username, pwd, code, pub_key, cookie)

    # do study
    post_study_record(cookie)


def start_with_workflow():
    init_logger()
    run(False)


if __name__ == '__main__':
    init_logger()
    run(True)
