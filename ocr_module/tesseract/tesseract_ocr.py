import os
import platform
import subprocess
from PIL import Image
from io import BytesIO
import base64
import re

SYSTEM_PLATFORM = platform.system()
THIS_PATH = os.path.dirname(__file__)

def is_need_keys() -> bool:
    return False

def get_result(img: bytes) -> str:
    if SYSTEM_PLATFORM == 'Linux':
        import pytesseract
    elif SYSTEM_PLATFORM == 'Windows':
        exe = os.path.join(THIS_PATH, "ocr-x86_64-windows-msvc.exe")
    else:
        raise Exception(f"tesseract 不支持该操作系统{SYSTEM_PLATFORM}, 仅支持 Windows 或 Linux")
    try:
        if (SYSTEM_PLATFORM == 'Windows'):
            out_bytes = subprocess.check_output([exe, '--validate-code-base64', img.decode()])
            return out_bytes.decode()
        elif (SYSTEM_PLATFORM == 'Linux'):
            digit_pattern = re.compile(r'\d+')
            image = Image.open(BytesIO(base64.b64decode(img.decode())))
            out_bytes = pytesseract.image_to_string(image, lang='eng', config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789')
            out_bytes = digit_pattern.findall(out_bytes)
        return out_bytes[0]
    except subprocess.CalledProcessError as e:
        raise Exception(f"ocr 识别失败，错误代码{e.returncode}")
