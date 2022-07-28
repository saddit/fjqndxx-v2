import base64
from io import BytesIO
import requests
from PIL import Image

_ENDPOINT = ''
_SECRET_KEY = ''


def set_keys(api_key, secret_key):
    global _ENDPOINT, _SECRET_KEY
    _ENDPOINT = api_key
    _SECRET_KEY = secret_key


def is_need_keys() -> bool:
    return True


def get_result(img: bytes) -> str:
    img = base64.standard_b64decode(img)
    buf = BytesIO()
    Image.open(BytesIO(img)) \
        .resize((157,52)) \
        .save(buf, format="JPEG")
    url = f"https://{_ENDPOINT}/vision/v3.2/ocr?language=en&detectOrientation=false"
    resp = requests.post(url, headers={
        "Ocp-Apim-Subscription-Key": _SECRET_KEY,
        "Content-type": "application/octet-stream"
    }, data=buf.getvalue(), timeout=10)
    body = resp.json()
    if resp.status_code != 200:
        raise Exception(f"识别失败: {body['error']['message']}")
    return body["regions"][0]["lines"][0]["words"][0]["text"]
