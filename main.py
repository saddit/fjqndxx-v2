import json
import logging
import os
from datetime import datetime
from functools import wraps

from api_module import main_api as api
from entity_module import Config
from exception import KnownException, SendInitException
from send_module import util as sendutil
from util import is_set

THIS_PATH = os.path.dirname(__file__)


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


def get_profile_from_config() -> Config:
    with open(os.path.join(THIS_PATH, 'config.json'), 'r', encoding='utf-8') as config:
        dt = json.loads(config.read())

    def save_file(c: Config):
        with open(os.path.join(THIS_PATH, 'config.json'), 'w', encoding='utf-8') as file:
            file.write(json.dumps(c.__dict__))

    conf = Config(dt, save_file)
    return conf


def get_profile_from_env() -> Config:
    s = os.environ['tk_config']
    dt = json.loads(s)
    # todo: save env
    return Config(dt, save = lambda c: c)


def start_study(conf: Config):
    course = api.get_last_course()
    api.study_log(conf.user_info, course)
    logging.info("study %s success", course.season_episode)


def check_config(conf: Config):
    now = datetime.now()
    tk_expire = datetime.fromtimestamp(conf.token_info.expire)
    rf_expire = datetime.fromtimestamp(conf.token_info.refreshExpire)
    if tk_expire <= now:
        if rf_expire <= now:
            raise KnownException("token and refreashToken has expired")
        logging.info("token expired, refeash token")
        conf.token_info = api.refresh_token(conf.token_info.refreshToken)
        
    if not is_set(conf.user_info.openid):
        logging.info("not found user info, get user info")
        conf.user_info = api.get_user_info(conf.user_info.id)


@catch_exception
def run(use_config: bool):
    logging.info("自动学习开始")
    # get default config
    conf = get_profile_from_config() if use_config else get_profile_from_env()
    if not is_set(conf):
        raise KnownException("找不到配置文件")
    # init api
    api.initalize(conf.token_info.token, conf.max_retry)
     # init sender
    sendutil.init_sender(conf.sender)
    # check token
    check_config(conf)
    # start study
    start_study(conf)
    # persist token and user info
    conf.persist()


def start_with_workflow():
    init_logger()
    logging.info("你正在使用GitHubAction,请确保secret已经配置")
    run(False)


def start_local():
    init_logger()
    logging.info("你正在使用本地服务,请确保填写了配置文件")
    run(True)


if __name__ == '__main__':
    start_local()
