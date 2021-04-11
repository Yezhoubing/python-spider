# -*- codeing=utf-8 -*-
# @Time:2021/4/1 16:49
# @Author:Ye Zhoubing
# @File: 爬取视频（简单）.py
# @software:PyCharm

#在91看剧爬取哲仁王后第二集，播放源为超级播

import requests
import re
import os
from concurrent.futures import ThreadPoolExecutor

def download(url,name):
    resp3 = requests.get(url)

    with open(f"video/{name}.ts", mode="wb") as ff:
        ff.write(resp3.content)

    print(f"{name}.ts","over")

    # 可以用urllib.request.urlretrieve(line,f"video/{name}.ts")


def merge_ts(download_path,hebing_path):

    #要求视频的顺序一致,都更改为4位数的数字
    for file in os.listdir(download_path):
        name = file.split('.')[0]
        os.rename(os.path.join(download_path, file), os.path.join(download_path, '%04d' % int(name) + ".ts"))  # ‘%04d’表示一共4位数
    all_ts = os.listdir(download_path)  # os.listdir返回指定的文件夹包含的文件或文件夹的名字的列表
    print(all_ts)
    with open(hebing_path, 'wb+') as f:
        for i in range(len(all_ts)):
            """
                os.path.join()
                函数功能：连接两个或更多的路径名组件
                
                如果各组件名首字母不包含’/’，则函数会自动加上
                
                如果有一个组件是一个绝对路径，则在它之前的所有组件均会被舍弃
                
                如果最后一个组件为空，则生成的路径以一个’/’分隔符结尾
            """
            ts_video_path = os.path.join(download_path, all_ts[i])
            f.write(open(ts_video_path, 'rb').read())
    print("合并完成！！")



def main():

    #在第二集的播放页面上爬取script中m3u8文件地址
    baseurl="https://www.91kanju.com/vod-play/54812-1-2.html"
    resp1=requests.get(baseurl)
    content1=resp1.text




    #用正则匹配到对应的url,m_url即m3u8文件链接
    obj=re.compile(r"url: '(?P<m_url>.*?)',",re.S)
    m_url=obj.search(content1).group("m_url")


    #获取m3u8文件内容并存出

    #urllib.request.urlretrieve(m_url,"1.m3u8")


    resp2=requests.get(m_url)

    with open("video/哲仁皇后.m3u8",mode="wb") as f:
        #open()不能创建文件夹
        f.write(resp2.content)
    print("哲仁皇后.m3u8","over")

    #从存储到本地m3u8文件中提取

    with open("video/哲仁皇后.m3u8",mode="r") as f:


        #从链接中下载ts文件
        with ThreadPoolExecutor(50) as t:
            x = 0
            for line in f:
                line = line.strip()  # 除去空格

                if line.startswith("#"):  # 舍弃#开头的行，只需要对应链接
                    continue

                t.submit(download,line,x)
                x=x+1

    #合并视频
    download_path=r"C:\Users\yezhoubing\Desktop\python\video\ts"
    hebing_path=r"C:\Users\yezhoubing\Desktop\python\video\哲仁皇后"
    merge_ts(download_path,hebing_path)




        #ts文件windows自带播放器就可打开，这里用网上下载的ts文件软件合并在一起
        # 视频存储在E:\ts文件合并软件\merge,合并后依旧为ts文件

if __name__ == '__main__':
    # main()
    download_path = r"C:\Users\yezhoubing\Desktop\python\video\ts"
    hebing_path = r"C:\Users\yezhoubing\Desktop\python\video\哲仁皇后.mp4"
    merge_ts(download_path, hebing_path)


    print("all over")