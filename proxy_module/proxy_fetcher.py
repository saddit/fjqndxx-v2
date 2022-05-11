import logging
import random
from exception import KnownException
from .proxy import fetchers


class ProxyFecher(object):

    cache_hosts: list[str]
    fetched: int

    def __init__(self):
        self.cache_hosts: list[str] = []
        self.fetched = 0

    def random_pop(self) -> str:
        if self.cache_hosts.__len__() == 0:
            self.fetch_new_hosts()
        idx = random.randint(0, len(self.cache_hosts) - 1)
        return self.cache_hosts.pop(idx)

    def empty(self) -> bool:
        return len(self.cache_hosts) == 0 and self.fetched == len(fetchers)

    def fetch_new_hosts(self):
        if self.fetched == len(fetchers):
            raise KnownException('已经更新过IP')
        logging.info("正在获取最新代理IP")
        self.cache_hosts.clear()
        while self.fetched < len(fetchers):
            try:
                fetcher = fetchers[self.fetched]
                for host in fetcher():
                    self.cache_hosts.append(host)
                break
            except Exception:
                logging.warning("正在查找可用IP代理...")
                self.fetched += 1
        if len(self.cache_hosts) == 0:
            raise KnownException("无可用代理IP")
        else:
            self.fetched += 1
