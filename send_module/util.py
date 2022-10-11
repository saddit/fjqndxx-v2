from importlib import import_module
import logging
from entity_module import Sender
from exception import SendInitException
from common_module.util import is_set


sender = Sender()


def enabled(enable: bool):
    sender.enabled = enable


def init_sender(sd: Sender):
    if not is_set(sd.type):
        return
    if not is_set(sd.key):
        raise SendInitException('缺少配置信息: sender.key')
    else:
        global sender
        sender = sd
        try:
            sender.executor = import_module(f"send_module.{sd.type}.sender")
        except ModuleNotFoundError:
            raise SendInitException("消息推送类型不存在，请更换类型")

        sender.enabled = True
        sender.executor.set_key(sd.key)
        if not is_set(sender.mode):
            sender.mode = 'fail'


def send_msg(content, success=True):
    if not sender.enabled:
        return
    if sender.can_send(success):
        res = sender.executor\
            .send(title="青年大学习打卡", content=f"状态: {'成功' if success else '失败'}\n\n信息{content}")
        if not res['success']:
            logging.warning(f"消息推送失败，原因：{res['message']}")
        else:
            logging.info(f"消息推送成功")
