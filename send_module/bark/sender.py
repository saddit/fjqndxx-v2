import requests

from exception.exceptions import UnexpectedException

sess = requests.session()
send_key = ""
send_url = ""


def set_key(key: str):
    global send_key, send_url
    url_key = key.split("#")
    if len(url_key) == 2 and url_key[0].startswith("http"):
        send_url = url_key[0]
        send_key = url_key[1]
    else:
        raise UnexpectedException("bark 推送需要配置 url#key 格式的send_key")


def send(title, content) -> dict:
    content.replace("\n", "\n\n")
    resp = sess.post(url=f"{send_url}/{send_key}/{title}/{content}")
    success = resp.ok
    return {
        'success': success,
        'message': resp.json()['Message'] if not success else '发送成功'
    }
