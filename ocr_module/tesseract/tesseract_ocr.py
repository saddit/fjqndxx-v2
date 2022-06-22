import os
import platform
import subprocess

SYSTEM_PLATFORM = platform.system()
THIS_PATH = os.path.dirname(__file__)

def is_need_keys() -> bool:
    return False


def get_result(img: bytes) -> str:
    if SYSTEM_PLATFORM == 'Linux':
        exe = os.path.join(THIS_PATH, "ocr-x86_64-linux-gnu")
    elif SYSTEM_PLATFORM == 'Windows':
        exe = os.path.join(THIS_PATH, "ocr-x86_64-windows-msvc.exe")
    else:
        raise Exception(f"tesseract 不支持该操作系统{SYSTEM_PLATFORM}, 仅支持Windows或Linux")
    
    try:
        out_bytes = subprocess.check_output([exe, '--validate-code-base64', img.decode()])
        return out_bytes.decode()
    except subprocess.CalledProcessError as e:
        raise Exception(f"ocr 识别失败，错误代码{e.returncode}")
