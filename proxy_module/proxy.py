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
    urls = ["https://www.89ip.cn/index_1.html",
            "https://www.89ip.cn/index_2.html",
            "https://www.89ip.cn/index_3.html"]
    for url in urls:
        r = requests.get(url,
                         timeout=10, verify=False)
        proxies = re.findall(
            r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
            r.text)
        for proxy in proxies:
            yield ':'.join(proxy)


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


def freeProxy03():
    """ 开心代理 """
    target_urls = ["http://www.kxdaili.com/dailiip.html",
                   "http://www.kxdaili.com/dailiip/2/1.html"]
    for url in target_urls:
        tree = requests.get(url, timeout=10).tree
        for tr in tree.xpath("//table[@class='active']//tr")[1:]:
            ip = "".join(tr.xpath('./td[1]/text()')).strip()
            port = "".join(tr.xpath('./td[2]/text()')).strip()
            yield "%s:%s" % (ip, port)


fetchers = [
    freeProxy02,
    freeProxy10,
    freeProxy04,
    freeProxy03,
]
