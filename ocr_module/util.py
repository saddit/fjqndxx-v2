from datetime import datetime
import importlib
import logging
import base64
import time

from exception.exceptions import KnownException

ocr_util = None

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

def get_validate_code(sess) -> str:
    max_try = 5
    has_try = 0
    while has_try < max_try:
        resp = sess.get(
            url=f"https://m.fjcyl.com/validateCode?0.{datetime.microsecond}&width=58&height=19&num=4")
        try:
            # noinspection PyUnresolvedReferences
            res = ocr_util.get_result(base64.b64encode(resp.content))
            logging.info('获取验证码成功')
            return res
        except Exception as e:
            logging.warning(f'获取验证码失败，原因:{e}')
            logging.warning(f'正在重试, 次数:{has_try}')
            has_try += 1
            time.sleep(1)

    if has_try == max_try:
        raise KnownException("验证码解析失败,请尝试更换方式或发issue寻求帮助")