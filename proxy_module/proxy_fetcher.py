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
        with open('proxies.txt', 'w+', encoding='utf-8') as host_file:
            self.cache_hosts = host_file.readlines()

    def random_pop(self) -> str:
        if len(self.cache_hosts) == 0:
            self.fetch_new_hosts()
        idx = random.randint(0, len(self.cache_hosts))
        return self.cache_hosts.pop(idx)

    def empty(self) -> bool:
        return len(self.cache_hosts) == 0 and self.fetched == len(fetchers)

    def fetch_new_hosts(self):
        if self.fetched == len(fetchers):
            raise KnownException('已经更新过IP')
        logging.info("正在获取最新代理IP")
        self.cache_hosts.clear()
        with open("proxies.txt", 'w+', encoding='utf-8') as host_file:
            fetcher = fetchers[self.fetched]
            for host in fetcher():
                self.cache_hosts.append(host)
                host_file.write(host+'\n')
        self.fetched += 1
