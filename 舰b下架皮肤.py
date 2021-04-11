# -*- codeing=utf-8 -*-
# @Time:2021/3/27 18:07
# @Author:Ye Zhoubing
# @File: 舰b下架皮肤.py
# @software:PyCharm

#使用selime模拟鼠标点击爬取网站上下架的碧蓝航线皮肤
#网址：https://bbs.nga.cn/read.php?tid=21916520&forder_by=postdatedesc&rand=910
from selenium import webdriver # 导入
import requests

def main():
    headers={
        "Referer": "https: // bdtj.tagtic.cn /",
        "User - Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 89.0.4389.90Safari / 537.36"

    }

    #网页是动态的，爬取内容不在网页上img中
    url="https://bbs.nga.cn/read.php?tid=21916520&forder_by=postdatedesc&rand=910"
    resp=requests.get(url,headers=headers)
    print(resp.text,)


if __name__ == '__main__':
    main()





