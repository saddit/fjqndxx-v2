import importlib
import json
import logging
import os
import time
from functools import wraps

import requests
import urllib3

from exception import KnownException, SendInitException

# 处理https警告
urllib3.disable_warnings()


CRYPT_NAME = "sm4"
CRYPT_MODE = "ecb"

sess = requests.session()

sess.verify = False
sess.headers.update({
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Host": "m.fjcyl.com",
    "Referer": "https://m.fjcyl.com/login"
})

ocr_util = None
encryptor = importlib.import_module(
    f"crypt_module.{CRYPT_NAME}.{CRYPT_NAME}_{CRYPT_MODE}")
send_util = {
    'enable': False,
    'mode': 'fail',
}


def catch_exception(func):
    @wraps(func)
    def catch(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SendInitException as se:
            send_util['enable'] = False
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
    send_msg(content=msg, success=False)
    if trace:
        logging.exception(f"异常信息: {msg}")
    else:
        logging.error(f"异常信息: {msg}")
    exit(-1)


def error_raise(msg: str):
    raise KnownException(msg)


def post_study_record():
    resp = sess.post(url="https://m.fjcyl.com/studyRecord")
    if resp.json().get('success'):
        logging.info("学习成功！")
    else:
        error_raise(f"学习失败,{resp.text}")


def post_login(username: str, pwd: str, pub_key):
    post_dict = {
        'userName': encryptor.encrypt(username, pub_key),
        'pwd': encryptor.encrypt(pwd, pub_key)
    }

    resp = sess.post(url="https://m.fjcyl.com/mobileNologin",
                     data=post_dict)

    if resp.status_code == requests.codes['ok']:
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

        send_config = config_json.get('send')
        accounts = config_json.get("extUsers")
        if send_config is not None:
            send_type = send_config.get('type')
            send_key = send_config.get('key')
            send_mode = send_config.get('mode')
    return username, pwd, pub_key, \
        send_type, send_key, send_mode, accounts


def get_profile_from_env():
    username = os.environ['username']
    pwd = os.environ['password']
    pub_key = os.environ['pubKey']
    send_type = os.environ['sendType']
    send_key = os.environ['sendKey']
    send_mode = os.environ['sendMode']
    ext_users = os.environ['extUsers']
    accounts = []
    if ext_users is not None and ext_users.__len__() > 1:
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
        send_type, send_key, send_mode, accounts


def login(username, pwd, pub_key):
    max_try = 5
    has_try = 0
    logging.info(f"正在登录尾号{username[-4:]}")
    while has_try < max_try:
        # do login
        try:
            post_login(username, pwd, pub_key)
            break
        except ConnectionError as e:
            logging.error(f'尾号{username[-4:]}登录失败，原因:{e}')
            logging.info(f'尝试重新登录，重试次数{has_try}')
            has_try += 1
            time.sleep(1)

    if has_try == max_try:
        error_raise(f"尾号{username[-4:]}尝试登录失败")


def init_sender(send_type, send_key, send_mode):
    if send_type is None or send_type == '':
        return
    if send_key is None or send_key == '':
        raise SendInitException('缺少配置信息: send_key')
    else:
        try:
            send_util['sender'] = importlib.import_module(
                f"send_module.{send_type}.sender")
        except ModuleNotFoundError:
            raise SendInitException("消息推送类型不存在，请更换类型")

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
                                       content=f"状态: {'成功' if success else '失败'}\n\n"
                                               f"信息 {content}")
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
            push_msg += f"尾号{account['username'][-4:]}失败:{e}\n"
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
def run(use_config: bool, use_proxy: bool = False):
    logging.info("自动学习开始")
    # get default config
    username, pwd, pub_key, \
        send_type, send_key, send_mode, \
        accounts = get_profile_from_config() if use_config else get_profile_from_env()
    # init sender
    init_sender(send_type, send_key, send_mode)
    # init proxy
    if use_proxy:
        init_proxy()
    # study proc
    if accounts is not None and len(accounts) > 0:
        if pwd is not None and username is not None and pwd != "" and username != "":
            accounts.append({"username": username, "pwd": pwd})
        multi_study(accounts, pub_key)
    else:
        single_study(username, pwd, pub_key)


def init_proxy():
    logging.info("正在尝试使用代理IP")
    module = importlib.import_module("proxy_module.proxy_fetcher")
    proxy = module.ProxyFecher()
    while not proxy.empty():
        ip = f"http://{proxy.random_pop()}"
        try:
            logging.info(f"正在测试 {ip}")
            sess.get("https://fjcyl.com/",
                         proxies={'https': ip}, timeout=8)

            logging.info(f"测试成功，使用{ip}代理请求")
            sess.proxies = {"https": ip}
            return
        except BaseException as e:
            logging.info(f"{ip} 不可用, {e}")
    error_raise("找不到可用代理IP")


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
