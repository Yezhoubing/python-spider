# -*- codeing=utf-8 -*-
# @Time:2021/4/4 15:22
# @Author:Ye Zhoubing
# @File: 多线程爬取图片.py
# @software:PyCharm
import requests
from bs4 import BeautifulSoup
from lxml import etree
import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor
import time

def download(url, name, Path):
    urllib.request.urlretrieve(url,f"{Path}{name}")
    print(name, "over")


def save_path():
    Path = "shipC/"
    if not os.path.exists(Path):
        os.mkdir(Path)
    return Path


def main(url):

    # 得到全舰娘列表
    resp = requests.get(url)
    # 创建文件夹
    path = save_path()

    # 从中得到每位舰娘立绘链接

    # / html / body / div / main / div / div / div[2] / div[2] / dl[838] / dt / a
    tree = etree.HTML(resp.text)

    ship_list = tree.xpath(f"/html/body/div/main/div/div/div[2]/div[2]/dl/dt/a/@href")

    for ship in ship_list:
        # 找到img链接
        head_url = url.split("/ship")[0]
        ship_url = head_url + ship
        resp = requests.get(ship_url)
        soup = BeautifulSoup(resp.text, "lxml")
        imgs = soup.find("div", class_="body").find_all("img")
        with ThreadPoolExecutor(100) as t:
            for img in imgs:
                src = img.get("src")
                filename = img.get("data-filename")
                src = src.replace("\\", "/")  # 将\替换为/
                src = head_url + src


                # 下载链接图片
                t.submit(download,src,filename,path)
                time.sleep(1)


if __name__ == '__main__':
    baseurl = "http://fleet.diablohu.com/ships/"
    main(baseurl)

    print("all over")