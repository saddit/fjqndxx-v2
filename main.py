import base64
import logging
import json
import requests

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from apscheduler.schedulers.blocking import BlockingScheduler

from baidu_image import ocr
from baidu_image import get_code_by_tesseract

sess = requests.session()

"""
脚本识别验证码使用的是百度的api，使用前请先申请百度ocr的key！或者更改baidu_image/ocr.py中的代码来使用你所知道的api
运行方法：
    1. 直接运行main.py
        将config.json.bak更名为config.json, 填写config数据为你自己的数据，然后直接运行即可
    2. 通过GitHubAction等自动化工具
        不运行此脚本，运行workflow.py, 以GithubAction为例，你需要添加五个secrets，分别为
        username, pwd, pub_key, ocr_api_key, ocr_secret_key
"""


def init_logger():
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format="[%(levelname)s]:%(message)s")


def get_validate_code() -> str:
    max_try = 5
    has_try = 0
    while has_try < max_try:
        resp = sess.get(url="https://m.fjcyl.com/validateCode?0.123123&width=58&height=19&num=4")
        res = ocr.netpic_ocr(base64.b64encode(resp.content))

        # 如果使用了其他api，以下内容都应进行修改
        if res.__contains__('error_msg'):
            logging.warning(f'get validate code - reason:{res["error_msg"]}')
            logging.warning(f'try again, tried times:{has_try}')
            has_try += 1
        else:
            logging.info('get validate code success')
            return res['words_result'][0]['words']


def get_validate_code2() -> str:
    resp = sess.get(url="https://m.fjcyl.com/validateCode?0.123123&width=58&height=19&num=4")
    with open('code.jpg', 'wb') as f:
        f.write(resp.content)
    return get_code_by_tesseract.get_code('code.jpg')


def post_study_record():
    resp = sess.post(url="https://m.fjcyl.com/studyRecord")
    if resp.json().get('success'):
        logging.info("study success recorded")
    else:
        logging.warning("study record failed")


def rsa_encrypt(public_key, src):
    public_key = '-----BEGIN PUBLIC KEY-----\n' + public_key + '\n-----END PUBLIC KEY-----'
    rsa_key = RSA.importKey(public_key)
    cipher = PKCS1_v1_5.new(rsa_key)
    return str(base64.b64encode(cipher.encrypt(src.encode('utf-8'))), 'utf-8')


def post_login(username: str, pwd: str, validate_code, pub_key):
    post_dict = {
        'userName': rsa_encrypt(pub_key, username),
        'pwd': rsa_encrypt(pub_key, pwd),
        'validateCode': rsa_encrypt(pub_key, validate_code)
    }

    resp = sess.post(url="https://m.fjcyl.com/mobileNologin",
                     data=post_dict)

    if resp.status_code == requests.codes.ok:
        logging.info('login ' + resp.json().get('errmsg'))
    else:
        logging.error(f'官方服务器发生异常,错误代码:{resp.status_code},信息:{resp.text}')
        raise RuntimeError('server error')

    if '验证码错误' in resp.json().get('errmsg'):
        raise ConnectionError("验证码错误")


def run(use_config: bool):
    logging.info("auto-study is Running")
    # get default config
    use_tesseract = False
    if use_config:
        with open('config.json', 'r') as config:
            jsons = json.loads(config.read())
            username = jsons.get('username')
            pwd = jsons.get('pwd')
            pub_key = jsons.get('rsaKey').get('public')
            if not jsons.get('ocr').get('sk'):
                use_tesseract = True
    else:
        username = input()
        pwd = input()
        pub_key = input()
        ocr.set_key(apikey=input(), secret_key=input())

    max_try = 5
    has_try = 0

    get_code = get_validate_code

    if use_tesseract:
        get_code = get_validate_code2

    while has_try < max_try:
        # get validate code
        code = get_code()
        # do login
        try:
            post_login(username, pwd, code, pub_key)
            break
        except ConnectionError as e:
            logging.error(f'登录失败，原因{e}')
            logging.info(f'尝试重新登录，重试次数{has_try}')
            has_try += 1

    if has_try == max_try:
        logging.error("重试登录失败，程序退出，截图日志发issue吧")
        return

    # do study
    post_study_record()


def start_with_workflow():
    init_logger()
    run(False)


if __name__ == '__main__':
    init_logger()
    scheduler = BlockingScheduler()
    scheduler.add_job(run, 'cron', day_of_week='0', args=(True,), hour=10, minute=0)
    scheduler.start()
