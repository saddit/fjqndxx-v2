import base64
import logging
import json
import os
import importlib
from functools import wraps

import requests

crypt_name = "sm4"
crypt_mode = "ecb"

sess = requests.session()
ocr_util = None
encryptor = importlib.import_module(f"crypt_module.{crypt_name}.{crypt_name}_{crypt_mode}")
send_util = {
    'enable': False,
    'mode': 'fail',
}

"""
脚本识别验证码使用的是百度的api，使用前请先申请百度ocr的key！或者更改baidu_image/ocr.py中的代码来使用你所知道的api
运行方法：
    1. 直接运行main.py
        将config.json.bak更名为config.json, 填写config数据为你自己的数据，然后直接运行即可
    2. 通过GitHubAction等自动化工具
        不运行此脚本，运行workflow.py, 以GithubAction为例，你需要添加五个secrets，分别为
        username, pwd, pub_key, ocr_api_key, ocr_secret_key
"""


def catch_exception(func):
    @wraps(func)
    def catch(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_exit(f"发生未知异常(请截图日志发issue)：{e}")
    return catch


def init_logger():
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format="[%(levelname)s]:%(message)s")


def error_exit(msg: str):
    logging.error(msg)
    send_msg(content=msg, success=False)
    exit(-1)


def get_validate_code() -> str:
    max_try = 5
    has_try = 0
    while has_try < max_try:
        resp = sess.get(url="https://m.fjcyl.com/validateCode?0.123123&width=58&height=19&num=4")
        try:
            # noinspection PyUnresolvedReferences
            res = ocr_util.get_result(base64.b64encode(resp.content))
            logging.info('获取验证码成功')
            return res
        except Exception as e:
            logging.warning(f'获取验证码失败，原因:{e}')
            logging.warning(f'正在重试, 次数:{has_try}')
            has_try += 1

    if has_try == max_try:
        error_exit("验证码解析失败,请尝试更换方式或发issue寻求帮助")


def post_study_record():
    resp = sess.post(url="https://m.fjcyl.com/studyRecord")
    if resp.json().get('success'):
        logging.info("学习成功！")
    else:
        error_exit("学习失败")


def post_login(username: str, pwd: str, validate_code, pub_key):
    post_dict = {
        'userName': encryptor.encrypt(username, pub_key),
        'pwd': encryptor.encrypt(pwd, pub_key),
        'validateCode': encryptor.encrypt(validate_code, pub_key)
    }

    resp = sess.post(url="https://m.fjcyl.com/mobileNologin",
                     data=post_dict)

    if resp.status_code == requests.codes.ok:
        if resp.json().get('success'):
            logging.info('login ' + resp.json().get('errmsg'))
        else:
            raise ConnectionError(resp.json().get('errmsg'))
    else:
        error_exit(f'官方服务器发生异常,错误代码:{resp.status_code},信息:{resp.text}')


def get_profile_from_config():
    with open('config.json', 'r', encoding='utf-8') as config:
        config_json = json.loads(config.read())
        username = config_json.get('username')
        pwd = config_json.get('pwd')
        pub_key = config_json.get('rsaKey').get('public')
        api_key = config_json.get('ocr').get('ak')
        secret_key = config_json.get('ocr').get('sk')
        ocr_type = config_json.get('ocr').get('type')
        sendConfig = config_json.get('send')
        if sendConfig is not None:
            send_type = sendConfig.get('type')
            send_key = sendConfig.get('key')
            send_mode = sendConfig.get('mode')
    return username, pwd, pub_key, \
           api_key, secret_key, ocr_type, \
           send_type, send_key, send_mode


def get_profile_from_env():
    username = os.environ['username']
    pwd = os.environ['password']
    pub_key = os.environ['pubKey']
    api_key = os.environ['ocrKey']
    secret_key = os.environ['ocrSecret']
    ocr_type = os.environ['ocrType']
    send_type = os.environ['sendType']
    send_key = os.environ['sendKey']
    send_mode = os.environ['sendMode']
    return username, pwd, pub_key, \
           api_key, secret_key, ocr_type, \
           send_type, send_key, send_mode


def login(username, pwd, pub_key):
    max_try = 5
    has_try = 0

    while has_try < max_try:
        # get validate code
        code = get_validate_code()
        # do login
        try:
            post_login(username, pwd, code, pub_key)
            break
        except ConnectionError as e:
            logging.error(f'登录失败，原因:{e}')
            logging.info(f'尝试重新登录，重试次数{has_try}')
            has_try += 1

    if has_try == max_try:
        error_exit("重试登录失败，程序退出，截图日志发issue吧")


def init_ocr(ocr_type: str, ak: str, sk: str):
    global ocr_util
    if ocr_type is None or ocr_type == '':
        ocr_type = "baidu_image"
    try:
        ocr_util = importlib.import_module(f"ocr_module.{ocr_type}.{ocr_type}_ocr")
    except ModuleNotFoundError:
        error_exit("ocr类型不存在,请更换类型")
    if ocr_util.is_need_keys():
        ocr_util.set_keys(ak, sk)
    logging.info(f"使用 OCR {ocr_type}")


def init_sender(send_type, send_key, send_mode):
    if send_type is None or send_type == '':
        return
    if send_key is None or send_key == '':
        error_exit('缺少配置信息: send_key')
    else:
        send_util['enable'] = True
        send_util['sender'] = importlib.import_module(f"send_module.{send_type}.sender")
        send_util['sender'].set_key(send_key)
        if send_mode is not None and send_mode != "":
            send_util['mode'] = send_mode


def send_msg(content, success=True):
    if not send_util['enable']:
        return
    if send_util['mode'] == 'both' \
            or (send_util['mode'] == 'fail' and not success) \
            or (send_util['mode'] == 'success' and success):
        res = send_util['sender'].send(title="青年大学习打卡",
                                       content=f"**状态：** {'成功' if success else '失败'}\n\n"
                                               f"**信息：** {content}")
        if not res['success']:
            logging.warning(f"消息推送失败，原因：{res['message']}")
        else:
            logging.info(f"消息推送成功")


@catch_exception
def run(use_config: bool):
    logging.info("自动学习开始")
    # get default config
    username, pwd, pub_key, \
    api_key, secret_key, ocr_type, \
    send_type, send_key, send_mode = get_profile_from_config() if use_config else get_profile_from_env()
    # init ocr module
    init_ocr(ocr_type, api_key, secret_key)
    # init sender
    init_sender(send_type, send_key, send_mode)
    # do login
    login(username, pwd, pub_key)
    # do study
    post_study_record()
    # send success message
    send_msg("打卡成功")


def start_with_workflow():
    init_logger()
    run(False)


if __name__ == '__main__':
    init_logger()
    run(True)
