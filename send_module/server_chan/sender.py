import requests

sess = requests.session()
send_key = ""


def set_key(key):
    global send_key
    send_key = key


def send(title, content) -> dict:
    content.replace("\n", "\n\n")
    resp = sess.post(url=f"https://sctapi.ftqq.com/{send_key}.send", data={
        'text': f"{title}",
        'desp': f"# {title}\n\n{content}"
    })
    res = resp.json()
    success = res['code'] == 0
    return {
        'success': success,
        'message': res['message'] if not success else '发送成功'
    }

