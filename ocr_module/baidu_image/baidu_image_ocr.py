from . import ocr


def is_need_keys():
    return True


def set_keys(ak, sk):
    ocr.set_key(ak, sk)


def get_result(img):
    res = ocr.netpic_ocr(img)
    if res.__contains__('error_msg'):
        raise Exception(res['error_msg'])
    else:
        return res['words_result'][0]['words']
