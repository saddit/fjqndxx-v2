import json
import logging
import os
import time
from functools import wraps

from api_module import main_api as api
from exception import KnownException, SendInitException
from ocr_module import util as ocrutil
from send_module import util as sendutil

MAX_TRY = 5


def catch_exception(func):
    @wraps(func)
    def catch(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SendInitException as se:
            sendutil.enabled(False)
            error_exit(f'{se}', False)
        except KnownException as ke:
            error_exit(f'{ke}', False)
        except BaseException as e:
            error_exit(f"请阅读异常提醒，如果无法解决请截图日志发issue)：{e}")
    return catch


def init_logger():
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format="[%(levelname)s]:%(message)s")


def error_exit(msg: str, trace=True):
    sendutil.send_msg(content=msg, success=False)
    if trace:
        logging.exception(f"异常信息: {msg}")
    else:
        logging.error(f"异常信息: {msg}")
    exit(-1)


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
        send_type, send_key, send_mode, accounts, api_key, secret_key, ocr_type


def get_profile_from_env():
    username = os.environ['username']
    pwd = os.environ['password']
    pub_key = os.environ['pubKey']
    send_type = os.environ['sendType']
    send_key = os.environ['sendKey']
    send_mode = os.environ['sendMode']
    ext_users = os.environ['extUsers']
    accounts = []

    api_key = os.environ['ocrKey']
    secret_key = os.environ['ocrSecret']
    ocr_type = os.environ['ocrType']

    if ext_users is not None and len(ext_users) > 1:
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
        send_type, send_key, send_mode, accounts, api_key, secret_key, ocr_type


def login(username, pwd, pub_key):
    has_try = 0
    logging.info(f"正在登录尾号{username[-4:]}")
    while has_try < MAX_TRY:
        code = api.get_validate_code()
        # do login
        try:
            api.post_login(username, pwd, pub_key, code)
            break
        except ConnectionError as e:
            logging.error(f'尾号{username[-4:]}登录失败，原因:{e}')
            logging.info(f'尝试重新登录，重试次数{has_try}')
            has_try += 1
            time.sleep(1)

    if has_try == MAX_TRY:
        raise KnownException(f"尾号{username[-4:]}尝试登录失败")


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
            api.post_study_record()
            push_msg += f"尾号{account['username'][-4:]}打卡成功\n"
        except KnownException as e:
            push_msg += f"尾号{account['username'][-4:]}失败:{e}\n"
            all_success = False
    push_msg += "全部打卡成功" if all_success else "部分打卡失败"
    sendutil.send_msg(push_msg, all_success)


def single_study(username, password, pub_key):
    logging.info("开始单人打卡")
    # do login
    login(username, password, pub_key)
    # do study
    api.post_study_record()
    # send success message
    sendutil.send_msg("打卡成功")


@catch_exception
def run(use_config: bool, use_proxy: bool = False):
    logging.info("自动学习开始")
    # get default config
    username, pwd, pub_key, \
        send_type, send_key, send_mode, \
        accounts, \
        api_key, secret_key, ocr_type = get_profile_from_config(
        ) if use_config else get_profile_from_env()
    # init sender
    sendutil.init_sender(send_type, send_key, send_mode)
    # init ocr
    ocrutil.init_ocr(ocr_type, api_key, secret_key)
    # init proxy
    api.init_proxy() if use_proxy else 0
    # study proc
    if accounts is not None and len(accounts) > 0:
        if pwd is not None and username is not None and pwd != "" and username != "":
            accounts.append({"username": username, "pwd": pwd})
        multi_study(accounts, pub_key)
    else:
        single_study(username, pwd, pub_key)


def start_with_docker():
    init_logger()
    logging.info("你正在使用docker运行,请确保环境变量存在")
    run(False, False)


def start_with_workflow():
    init_logger()
    logging.info("你正在使用GitHubAction,请确保secret已经配置")
    run(False, True)


def start_local():
    init_logger()
    logging.info("你正在使用本地服务,请确保填写了配置文件")
    run(True, False)


if __name__ == '__main__':
    start_local()
