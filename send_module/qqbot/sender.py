import requests

sess = requests.session()
access_token = ""
api_url = ""
user_id = ""

def set_access_token(token):
    global access_token
    access_token = token

def set_api_url(url):
    global api_url
    api_url = url

def set_user_id(id):
    global user_id
    user_id = id

def send(title, content) -> dict:
    resp = sess.post(url=f"{api_url}", data={
        "access_token" : f"{access_token}",
        "user_id" : f"{user_id}",
        "message" : f"{title}\n\n{content}"
    })
    res = resp.json()
    success = res['status'] == 'ok'
    return {
        'success': success,
        'message': res['status'] if not success else '发送成功'
    }

