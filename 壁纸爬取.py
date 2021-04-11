# -*- codeing=utf-8 -*-
# @Time:2021/3/24 9:20
# @Author:Ye Zhoubing
# @File: 壁纸爬取.py
# @software:PyCharm
#爬取优美图库动漫壁纸
import requests
from bs4 import BeautifulSoup
import time

def main():
    #源网站
    url="https://www.umei.cc/katongdongman/dongmanbizhi/"
    resp=requests.get(url)
    resp.encoding="utf-8"
    content=resp.text
    soup=BeautifulSoup(content,"lxml")
    link_list=soup.find("div",class_="TypeList").find_all("a")
    for link in link_list:
        a=link.get("href")
        # print(a)
        child_resp=requests.get(a)
        child_resp.encoding="utf-8"  #防止出现图名片乱码现象
        child_content=child_resp.text
        child_soup=BeautifulSoup(child_content,"lxml")
        img_link=child_soup.find("img").get("src")
        img_name=child_soup.find("img").get("alt")
        # print(img_link)

        #下载img_link中的图片，并用img中alt属性命名
        img_resp=requests.get(img_link)
        img_content=img_resp.content #此时存储的是字节
        with open("壁纸爬取/"+img_name+".jpg",mode="wb") as f:
            f.write(img_content)

        print(img_name,"完成")
        time.sleep(1)#间隔1秒

    print("全部完成")




if __name__ == '__main__':
    main()