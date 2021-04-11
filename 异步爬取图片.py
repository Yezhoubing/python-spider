# -*- codeing=utf-8 -*-
# @Time:2021/4/3 20:48
# @Author:Ye Zhoubing
# @File: 异步爬取图片.py
# @software:PyCharm


import requests
from bs4 import BeautifulSoup
from lxml import etree
import os
import aiohttp
import asyncio
import aiofiles
import time

async def download(url,name,Path):

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            async with aiofiles.open(f"{Path}{name}",mode="wb") as fp:
                await fp.write(await resp.read())

    print(name,"over")


def save_path():
    Path = "shipC/"
    if not os.path.exists(Path):
        os.mkdir(Path)
    return Path


async def main(url):
    tasks=[]
    #得到全舰娘列表
    resp=requests.get(url)
    #创建文件夹
    path = save_path()

    #从中得到每位舰娘立绘链接
    # / html / body / div / main / div / div / div[2] / div[2] / dl[838] / dt / a
    tree = etree.HTML(resp.text)
    ship_list = tree.xpath("/html/body/div/main/div/div/div[2]/div[2]/dl/dt/a/@href")

    for ship in ship_list:
        #找到img链接
        head_url = url.split("/ship")[0]
        ship_url = head_url+ship
        resp = requests.get(ship_url)
        soup = BeautifulSoup(resp.text,"lxml")
        imgs = soup.find("div", class_="body").find_all("img")
        for img in imgs:
            src = img.get("src")
            filename = img.get("data-filename")
            src = src.replace("\\","/") #将\替换为/
            src = head_url+src


            #下载链接图片
            tasks.append(asyncio.create_task(download(src,filename,path)))
            await asyncio.wait(tasks)
            time.sleep(1)




     

    


if __name__ == '__main__':
    baseurl = "http://fleet.diablohu.com/ships/"
    asyncio.run(main(baseurl))

    print("all over")
