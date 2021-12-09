import base64
import logging
import json
import os
import importlib
import time
from functools import wraps

import requests

from exception.exceptions import KnownException

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
        except BaseException as e:
            error_exit(f"请阅读异常提醒，如果无法解决请截图日志发issue)：{e}")

    return catch


def init_logger():
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format="[%(levelname)s]:%(message)s")


def error_exit(msg: str):
    send_msg(content=msg, success=False)
    logging.exception(f"异常信息: {msg}")
    exit(-1)


def error_raise(msg: str):
    raise KnownException(msg)


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
            time.sleep(1)

    if has_try == max_try:
        error_raise("验证码解析失败,请尝试更换方式或发issue寻求帮助")


def post_study_record():
    resp = sess.post(url="https://m.fjcyl.com/studyRecord")
    if resp.json().get('success'):
        logging.info("学习成功！")
    else:
        error_raise("学习失败")


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
            logging.info(username[-4:] + ' login ' + resp.json().get('errmsg'))
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
        send_config = config_json.get('send')
        accounts = config_json.get("extUsers")
        if send_config is not None:
            send_type = send_config.get('type')
            send_key = send_config.get('key')
            send_mode = send_config.get('mode')
    return username, pwd, pub_key, \
           api_key, secret_key, ocr_type, \
           send_type, send_key, send_mode, accounts


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
    ext_users = os.environ['extUsers']
    accounts = []
    for userLine in ext_users.split('\n'):
        usr_split = userLine.split(" ")
        account = {
            "username": None,
            "pwd": None
        }
        if len(usr_split) > 0:
            account['username'] = usr_split[0]
        if len(usr_split) > 1:
            account['pwd'] = usr_split[1]
        accounts.append(account)
    return username, pwd, pub_key, \
           api_key, secret_key, ocr_type, \
           send_type, send_key, send_mode, accounts


def login(username, pwd, pub_key):
    max_try = 5
    has_try = 0
    logging.info(f"正在登录尾号{username[-4:]}")
    while has_try < max_try:
        # get validate code
        code = get_validate_code()
        # do login
        try:
            post_login(username, pwd, code, pub_key)
            break
        except ConnectionError as e:
            logging.error(f'尾号{username[-4:]}登录失败，原因:{e}')
            logging.info(f'尝试重新登录，重试次数{has_try}')
            has_try += 1
            time.sleep(1)

    if has_try == max_try:
        error_raise(f"尾号{username[-4:]}尝试登录失败")


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
        try:
            send_util['sender'] = importlib.import_module(f"send_module.{send_type}.sender")
        except ModuleNotFoundError:
            error_exit("消息推送类型不存在，请更换类型")

        send_util['enable'] = True
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


def multi_study(accounts, pub_key):
    logging.info(f"开始多人打卡，人数{len(accounts)}")
    push_msg = ""
    all_success = True
    for account in accounts:
        if account['username'] is None or account['pwd'] is None:
            logging.warning("多人打卡配置存在错误,将跳过部分用户,请检查配置的用户名密码格式")
            continue

        try:
            login(account['username'], account['pwd'], pub_key)
            post_study_record()
            push_msg += f"尾号{account['username'][-4:]}打卡成功\n"
        except KnownException as e:
            push_msg += f"{e}\n"
            all_success = False
    push_msg += "全部打卡成功" if all_success else "部分打卡失败"
    send_msg(push_msg, all_success)


def single_study(username, password, pub_key):
    logging.info("开始单人打卡")
    # do login
    login(username, password, pub_key)
    # do study
    post_study_record()
    # send success message
    send_msg("打卡成功")


@catch_exception
def run(use_config: bool):
    logging.info("自动学习开始")
    # get default config
    username, pwd, pub_key, \
    api_key, secret_key, ocr_type, \
    send_type, send_key, send_mode, \
    accounts = get_profile_from_config() if use_config else get_profile_from_env()
    # init ocr module
    init_ocr(ocr_type, api_key, secret_key)
    # init sender
    init_sender(send_type, send_key, send_mode)
    # study proc
    if accounts is not None and len(accounts) > 0:
        if pwd != "" and username != "":
            accounts.append({"username": username, "pwd": pwd})
        multi_study(accounts, pub_key)
    else:
        single_study(username, pwd, pub_key)


def start_with_workflow():
    init_logger()
    logging.info("你正在使用GitHubAction,请确保secret已经配置")
    run(False)


if __name__ == '__main__':
    init_logger()
    logging.info("你正在使用本地服务,请确保填写了配置文件")
    run(True)
