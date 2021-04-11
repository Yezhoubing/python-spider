# -*- codeing=utf-8 -*-
# @Time:2021/3/27 19:45
# @Author:Ye Zhoubing
# @File: 舰b立绘.py
# @software:PyCharm
import requests
from bs4 import BeautifulSoup
from lxml import etree
import os
import urllib.request
import time
from concurrent.futures import ThreadPoolExecutor


#推荐使用多线程提高效率
def main():


    path=create_path()

    baseurl = "https://azurlane.koumakan.jp/List_of_Ships"
    url = "https://azurlane.koumakan.jp"
    resp = requests.get(baseurl)
    resp.encoding = "UTF-8"
    content = resp.text
    tree = etree.HTML(content)

    # 在本地td差一个位置
    # tds=tree.xpath('//table/tbody/tr[16]/td[2]/a/@href')

    tds = tree.xpath('//table/tbody/tr/td[2]/a/@href')
    #多线程
    with ThreadPoolExecutor(50) as t:
        for i in tds:
            t.submit(Get_img,baseurl,url,i,path)








def Get_img(baseurl,url,i,path):

    # 这里rstrip会将jp中的p删掉
    gallery_url = baseurl.rstrip("/List_of_Ships") + "p" + i + "/Gallery"

    td_name = i.strip("/")
    # 中文名称在”https://azurlane.koumakan.jp/name“中，可以考虑改善代码
    # 用中文名称
    name = Get_name(url + i)

    # print(gallery_url)
    # 在gallery页面上
    gallery_resp = requests.get(gallery_url)
    gallery_content = gallery_resp.text
    gallery_soup = BeautifulSoup(gallery_content, "html.parser")
    divs = gallery_soup.find_all("div", class_="shipskin-image res-h")
    x = 0
    for div in divs:
        href_list = div.find_all("a", class_="image")
        for j in href_list:
            href = j.get("href")

            file_url = url + href
            # 在file页面上
            file_resp = requests.get(file_url)
            file_content = file_resp.text
            file_soup = BeautifulSoup(file_content, "html.parser")
            file_href = file_soup.find("div", class_="fullImageLink").find("a").get("href")

            img_url = url + file_href
            x = x + 1
            auto_down(img_url, f"{path}/{name}({x}).png")

            print(name, "over")
            time.sleep(1)


def create_path():
    path = '舰b立绘（中）/'
    if not os.path.exists(path):
        os.mkdir(path)
    return path

#抓捕异常，但可能会陷入死循环下载，建议在网络良好的时候下载
def auto_down(url,filename):
    try:
        urllib.request.urlretrieve(url,filename)
    except urllib.error.ContentTooShortError:
        print ('Network conditions is not good.Reloading.')
        auto_down(url,filename)

def Get_name(url):
    name_resp = requests.get(url)
    # print(name_resp.text)
    name_resp.encoding = "utf-8"
    name_content = name_resp.text
    # print(name_content)
    soup = BeautifulSoup(name_content, "html.parser")
    name = soup.find("span", lang="zh").text
    return name



if __name__ == '__main__':
    main()
    print("all over")

