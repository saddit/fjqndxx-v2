import importlib
import logging

from exception.exceptions import KnownException

ocr_util = None

def img_ocr(img: bytes) -> str:
    return ocr_util.get_result(img)

def init_ocr(ocr_type: str, ak: str, sk: str):
    global ocr_util
    if ocr_type is None or ocr_type == '':
        ocr_type = "baidu_image"
    try:
        ocr_util = importlib.import_module(
            f"ocr_module.{ocr_type}.{ocr_type}_ocr")
    except ModuleNotFoundError:
        raise KnownException("ocr类型不存在,请更换类型")

    if ocr_util.is_need_keys():
        ocr_util.set_keys(ak, sk)
    logging.info(f"使用 OCR {ocr_type}")