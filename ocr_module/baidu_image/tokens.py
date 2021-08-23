import requests


def get_token(ak, sk) -> str:
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token' \
           f'?grant_type=client_credentials&client_id={ak}&client_secret={sk}'
    response = requests.get(host)
    if response.ok:
        return response.json().get('access_token')
    else:
        raise RuntimeError(response.json().get('error_description'))
