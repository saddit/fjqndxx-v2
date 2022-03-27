import requests
import re
from lxml import etree


def freeProxy04():
    """ 蝶鸟IP """
    url = "https://www.dieniao.com/FreeProxy.html"
    tree = etree.HTML(requests.get(url, verify=False, timeout=10).content)
    for li in tree.xpath("//div[@class='free-main col-lg-12 col-md-12 col-sm-12 col-xs-12']/ul/li")[1:]:
        ip = "".join(li.xpath('./span[1]/text()')).strip()
        port = "".join(li.xpath('./span[2]/text()')).strip()
        yield "%s:%s" % (ip, port)


def freeProxy10():
    """ 89免费代理 """
    r = requests.get("https://www.89ip.cn/index_1.html",
                     timeout=10, verify=False)
    proxies = re.findall(
        r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
        r.text)
    for proxy in proxies:
        yield ':'.join(proxy)


def freeProxy08():
    """ 小幻代理 """
    urls = ['https://ip.ihuan.me/address/5Lit5Zu9.html']
    for url in urls:
        r = requests.get(url, timeout=10)
        proxies = re.findall(
            r'>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</a></td><td>(\d+)</td>', r.text)
        for proxy in proxies:
            yield ":".join(proxy)


def freeProxy02():
    """
    代理66 http://www.66ip.cn/
    :return:
    """
    url = "http://www.66ip.cn/mo.php"

    resp = requests.get(url, timeout=10)
    proxies = re.findall(
        r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})', resp.text)
    for proxy in proxies:
        yield proxy


fetchers = [
    freeProxy02,
    freeProxy10,
    freeProxy04,
]
