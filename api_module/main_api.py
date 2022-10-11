from functools import wraps
import logging
import requests
import urllib3
from api_module.sign import get_ts, use_sign
from entity_module import UserInfo, TokenInfo, CourseInfo
from exception.exceptions import KnownException

# 处理https警告
urllib3.disable_warnings()

max_retry = 5

base = "https://api.iyunci.cn/fjqndxx/v1/app/big_study"

sess = requests.session()
sess.verify = False
sess.headers.update({
    "Host": "api.iyunci.cn",
    "Origin": "https://fjqndxx.iyunci.cn",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.20(0x18001442) NetType/WIFI Language/zh_CN",
    "Timestamp": 0,
    "Sign": "",
    "Authorization": ""
})


def __retry_api(func):
    @wraps(func)
    def retry(*args, **kwargs):
        cnt = 1
        while cnt <= max_retry:
            try:
                return func(*args, **kwargs)
            except KnownException as e:
                logging.error("api-err: %s, retry %d", e, cnt)
                cnt += 1
        if cnt == max_retry:
            raise KnownException("exceeded max retries")
    return retry


def initalize(tk: str, retry: int):
    global max_retry
    max_retry = retry
    sess.headers.update({
        "Authorization": tk
    })


@__retry_api
def study_log(user: UserInfo, course: CourseInfo):
    """/study/log

    Args:
        user (UserInfo): studying user
        course (CourseInfo): course to study
    """
    body = {
        "userId": user.id,
        "id_number": user.id_number,
        "name": user.name,
        "openid": user.openid,
        "platform": user.platform,
        "course": course.id,
        "course_name": course.season_episode,
        "identify": 0,
        "study_time": get_ts() - 60 * 1000 * 5,  # five minutes ago
    }
    ts, sign = use_sign(body)
    resp = sess.post(f"{base}/study/log", json=body, headers={
        "Timestamp": ts,
        "Sign": sign
    })
    check_resp(resp)


@__retry_api
def get_last_course() -> CourseInfo:
    """/course/get

    Returns:
        CourseInfo: last course infomation
    """
    param = {"platform": 3}
    ts, sign = use_sign(param)
    resp = sess.get(f"{base}/course/get", params=param, headers={
        "Timestamp": ts,
        "Sign": sign
    })
    return CourseInfo(dt=check_resp(resp))


@__retry_api
def get_user_info(id: int) -> UserInfo:
    """/user/refresh

    Args:
        id (int): user_id

    Returns:
        UserInfo: user infomation
    """
    param = {"id": id}
    ts, sign = use_sign(param)
    resp = sess.post(f"{base}/user/refresh", json=param, headers={
        "Timestamp": ts,
        "Sign": sign
    })
    return UserInfo(dt=check_resp(resp))


@__retry_api
def refresh_token(refresh_token: str) -> TokenInfo:
    """/user/refreshToken

    Args:
        refresh_token (str): refresh token

    Returns:
        TokenInfo: new token info
    """
    resp = sess.get(f"{base}/user/refreshToken?refreshToken={refresh_token}", headers={
        "Timestamp": str(get_ts())
    })
    info = TokenInfo(dt=check_resp(resp))
    sess.headers['Authorization'] = info.token
    return info


def login_by_mp(unionid: str, mp_openid: str) -> tuple[TokenInfo, UserInfo]:
    body = {
        "unionid": unionid,
        "mp_openid": mp_openid
    }
    ts, sign = use_sign(body)
    resp = sess.post(f"{base}/user/loginByMp", json=body, headers={
        "Timestamp": ts,
        "Sign": sign
    })
    dt = check_resp(resp)
    usr_info = UserInfo(dt['userInfo'])
    tk_info = TokenInfo(dt)
    sess.headers['Authorization'] = tk_info.token
    return tk_info, usr_info


def check_resp(resp: requests.Response) -> dict:
    res = resp.json()
    if res['code'] != 1000:
        raise KnownException(f"bad request to {resp.url}: {res['message']}")
    return res['data']
