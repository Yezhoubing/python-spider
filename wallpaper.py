

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/11 16:31
# @Author  : huni
# @File    : 好看的壁纸图片爬取.py
# @Software: PyCharm
import requests
from lxml import etree
import os
from threading import Thread
from queue import Queue

class CrawlInfo(Thread):
    def __init__(self,url_queue,html_queue):
        Thread.__init__(self)
        self.url_queue = url_queue
        self.html_queue = html_queue
    def run(self):
        while self.url_queue.empty() == False:
            url = self.url_queue.get()
            reponse = requests.get(url=url,headers=headers)
            if reponse.status_code == 200:
                self.html_queue.put(reponse.text)

class ParseInfo(Thread):
    def __init__(self,html_queue):
        Thread.__init__(self)
        self.html_queue = html_queue
    def run(self):
        while self.html_queue.empty() == False:
            tree = etree.HTML(self.html_queue.get())
            li_list = tree.xpath('/html/body/div[4]/ul/li')
            for li in li_list:
                href = li.xpath('./a[1]/@href')[0]
                resp1 = requests.get(url=href, headers=headers).text
                tree1 = etree.HTML(resp1)
                src = tree1.xpath('//*[@id="showimg"]/a[4]/img/@src')[0]
                jpg_data = requests.get(url=src, headers=headers).content
                jpg_name = src.split('/')[-1]
                jpg_path = m_path + f'/{jpg_name}'

                with open(jpg_path, 'wb') as fp:
                    fp.write(jpg_data)
                    print(jpg_name, '下载完成')


if __name__ == '__main__':
    url_queue = Queue()
    html_queue=Queue()
    m_path = './壁纸爬取'
    if not os.path.exists(m_path):
        os.mkdir(m_path)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
    for i in range(1,6):
        # f / format()格式化操作，相当于format()函数
        url = f'https://www.3gbizhi.com/tag/dongman/{i}.html'
        url_queue.put(url)

    crawl_list = []
    for i in range(5):
        Crawl = CrawlInfo(url_queue, html_queue)
        crawl_list.append(Crawl)
        Crawl.start()

    for crawl in crawl_list:
        crawl.join()

    parse_list = []
    for i in range(20):
        parse = ParseInfo(html_queue)
        parse_list.append(parse)
        parse.start()

    for parse in parse_list:
        parse.join()



