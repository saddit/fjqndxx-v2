import importlib
import logging
from exception import SendInitException
from util import is_set


send_util = {
    'enable': False,
    'mode': 'fail',
}

def enabled(enable: bool):
    send_util['enable'] = enable


def init_sender(send_type, send_key, send_mode):
    if not is_set(send_type):
        return
    if not is_set(send_key):
        raise SendInitException('缺少配置信息: send_key')
    else:
        try:
            send_util['sender'] = importlib.import_module(
                f"send_module.{send_type}.sender")
        except ModuleNotFoundError:
            raise SendInitException("消息推送类型不存在，请更换类型")

        send_util['enable'] = True
        send_util['sender'].set_key(send_key)
        if not is_set(send_mode):
            send_util['mode'] = send_mode


def send_msg(content, success=True):
    if not send_util['enable']:
        return
    if send_util['mode'] == 'both' \
            or (send_util['mode'] == 'fail' and not success) \
            or (send_util['mode'] == 'success' and success):
        res = send_util['sender'].send(title="青年大学习打卡",
                                       content=f"状态: {'成功' if success else '失败'}\n\n"
                                               f"信息 {content}")
        if not res['success']:
            logging.warning(f"消息推送失败，原因：{res['message']}")
        else:
            logging.info(f"消息推送成功")
