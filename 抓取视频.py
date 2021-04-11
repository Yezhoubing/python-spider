# -*- codeing=utf-8 -*-
# @Time:2021/3/24 20:59
# @Author:Ye Zhoubing
# @File: 抓取视频.py
# @software:PyCharm

#下载梨视频
import requests
import os
import urllib.request
from bs4 import BeautifulSoup

def main():
    url="https://www.pearvideo.com/video_1724469"

    name_resp=requests.get(url)
    soup=BeautifulSoup(name_resp.text,"lxml")
    name=soup.find("h1",class_="video-tt" ).text
    print(name)

    # 获得_后的数字，url.split("_")为两部分，取第二个部分
    cont = url.split("_")[1]
    # print(cont)

    video_url=f"https://www.pearvideo.com/videoStatus.jsp?contId={cont}&mrd=0.6290876478265983"
    headers={
        # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Referer": "https://www.pearvideo.com/video_1724469" # 防盗链,意义:本次请求是由哪个url产⽣的,告诉服务器该网页是从哪个页面链接过来的，服务器因此可以获得一些信息用于处理。
    }

    resp=requests.get(video_url,headers=headers)
    content=resp.json()
    # print(content) #此时链接还是404

    systemtime=content["systemTime"]
    src=content["videoInfo"]["videos"]["srcUrl"]
    #替换
    src=src.replace(systemtime,"cont-"+cont)
    # print(src)

    #储存视频
    path="video/" #当前路径下创建video文件夹：./video或者video
    if not os.path.exists(path):
        os.mkdir(path)

    urllib.request.urlretrieve(src, f"{path}{name}.mp4")







if __name__ == '__main__':
    main()
    print("success")


