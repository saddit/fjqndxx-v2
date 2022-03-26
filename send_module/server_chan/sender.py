import requests

send_sess = requests.session()
send_key = ""


def set_key(key):
    global send_key
    send_key = key


def send(title, content) -> dict:
    content.replace("\n", "\n\n")
    resp = send_sess.post(url=f"https://sctapi.ftqq.com/{send_key}.send", data={
        'text': f"{title}",
        'desp': f"# {title}\n\n{content}"
    })
    send_res = resp.json()
    success = send_res['code'] == 0
    return {
        'success': success,
        'message': send_res['message'] if not success else '发送成功'
    }

