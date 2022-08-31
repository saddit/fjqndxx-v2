import base64
from io import BytesIO

from PIL import Image

import pytesseract


def is_need_keys() -> bool:
    return False


def get_result(img: bytes) -> str:
    img = base64.standard_b64decode(img)
    gray = Image.open(BytesIO(img)).resize((157,52))
    return pytesseract.image_to_string(gray).strip()
