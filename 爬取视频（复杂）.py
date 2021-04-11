# -*- codeing=utf-8 -*-
# @Time:2021/4/1 19:54
# @Author:Ye Zhoubing
# @File: 爬取视频（复杂）.py
# @software:PyCharm
#在云播tv爬取咒术回战第一集
#由于反爬，还是会出现不少问题，用不同IP去尝试
"""
    首先找到第一层的m3u8,再找到第二层真正的m3u8,
    从中下载ts文件，再用其中的key解密，合并ts为mp3
"""
import requests
import aiohttp
import asyncio
import aiofiles
import urllib.request
import re
import os
from Crypto.Cipher import AES #需要安装pycryptodome包


def get_first_m3u8(text):
    #用正则匹配第一层m3u8链接
    obj=re.compile(r'var player_aaaa={.*?"url":"(?P<url>.*?)".*?}',re.S)
    url=obj.search(text).group("url")
    return url.replace('\\','') #将\删除


def save_m3u8(url,x):
    """
    将m3u8保存到本地
    """

    #建立保存路径
    path="./video/咒术回战/"
    if not os.path.exists(path):
        os.mkdir(path)
        #存为1.m3u8
    urllib.request.urlretrieve(url,f"{path}{x}.m3u8")

    print(f"{x},m3u8","saved")

async def aio_download():
    #提取出每一个ts文件
    tasks=[]
    async with aiofiles.open("video/咒术回战/2.m3u8",mode="r") as f:
        #TCPConnector维持链接池，限制并行连接的总量，当池满了，有请求退出再加入新请求。默认是100，limit=0的时候是无限制
        #verify_ssl (布尔类型) –对HTTPS请求验证SSL证书(默认是验证的)。如果某些网站证书无效的话也可禁用。
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64,verify_ssl=False)) as session: #提前准备好session
            x = 0
            async for line in f:
                line=line.strip() #去掉空格和换行\n
                if line.startswith("#"):
                    continue
                ts_url = line
                #ts文件存储用四位数命名
                name = "%04d" % (x+1)
                x = x+1
                tasks.append(asyncio.create_task(ts_download(session,ts_url,name)))
                # time.sleep(1)
            await asyncio.wait(tasks) #等待任务结束

async def ts_download(session,url,name):
    #下载对应的ts文件,由于反爬可能会强制断开，所以用try
    try:
        await asyncio.sleep(2) #休眠2秒
        async with session.get(url) as resp:
            #前提咒术回战（ts）文件夹存在，否则会报错
            async with aiofiles.open(f"video/咒术回战（ts）/{name}.ts",mode="wb") as f:
               await f.write(await resp.content.read())
            print(f"{name}.ts","over")
    except aiohttp.client_exceptions.ServerDisconnectedError:
        await asyncio.wait(asyncio.create_task(ts_download(session, url, name)))


def get_key(url):
    resp = requests.get(url)

    return resp.text

async def aio_dec(key):
    tasks = []
    async with aiofiles.open("video/咒术回战/2.m3u8", mode="r") as f:
        x = 0
        async for line in f:
            line = line.strip()  # 去掉空格和换行\n
            if line.startswith("#"):
                continue
            name = "%04d" % (x+1)
            tasks.append(asyncio.create_task(dec_ts(name, key)))
            x = x+1
        await asyncio.wait(tasks)  # 等待任务结束

async def dec_ts(name,key):
    #记得明文,密钥,IV都要编码
   aes=AES.new(key=key.encode("utf-8"),IV=b"0000000000000000",mode=AES.MODE_CBC) #IV表示偏移量，0的个数与key保持一致
   #这里的\表示续行符，open() f1,f2
   async with aiofiles.open(f"video/咒术回战（ts）/{name}.ts",mode="rb") as f1,\
       aiofiles.open(f"video/咒术回战（dec_ts）/dec_{name}.ts",mode="wb") as f2:
            #捕获所有异常
            try:
                bs=await f1.read()
                await f2.write(aes.decrypt(bs)) #将解密内容写入f2
                print(f"dec_{name}","over")
            except Exception as e:
                print("The part is an advertisement")

def merge_ts(download_path, hebing_path):
    #这种方法有问题
    # datalist=[]
    # x=0
    # path="video/咒术回战（dec_ts）"
    # length=os.listdir(path)
    # for i in range(100):
    #     name = "%04d" % (x+1)
    #     datalist.append(f"{path}/dec_{name}.ts")
    #     x = x+1
    # total="+".join(datalist)
    # order=f"copy /b {total} 咒术回战1.mp4"
    # os.system(order)

    # 要求视频的顺序一致,都更改为4位数的数字

    all_ts = os.listdir(download_path)  # os.listdir返回指定的文件夹包含的文件或文件夹的名字的列表
    # print(all_ts)
    with open(hebing_path, 'wb+') as f:
        for i in range(len(all_ts)):

            ts_video_path = os.path.join(download_path, all_ts[i])
            f.write(open(ts_video_path, 'rb').read())
    print("合并完成！！")

def main(url):
    resp = requests.get(url)


    m3u8_1_url = get_first_m3u8(resp.text)

    #将url1_url的m3u8文件存在本地
    save_m3u8(m3u8_1_url,1)

    # #获取第二层m3u8链接并保存下来
    with open("video/咒术回战/1.m3u8",mode="r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            tail = line
            m3u8_2_url = m3u8_1_url.split("/20200928")[0]+tail

            save_m3u8(m3u8_2_url,2)
    #下载2.m3u8文件中的ts
    asyncio.run(aio_download())
    #另一种写法，解决循环停止错误
    loop = asyncio.get_event_loop()
    loop.run_until_complete(aio_download())
    #报错的时候尝试一下用热点


    #获取解密的key
    # https: // ts2.chinalincoln.com: 9999 / 20200928 / pvJswIZH / 1000kb / hls / key.key
    #从2.m3u8中提取uri中key的链接
    with open("video/咒术回战/2.m3u8", mode="r") as f:
        content = f.read() #read()方法直接将文件中的内容转换为字符串
        obj=re.compile(r'URI="(?P<key>.*?)"',re.S)
        key_url=obj.search(content).group("key")
        key=get_key(key_url) #拿到key

    # #利用key解密ts文件
    asyncio.run(aio_dec(key))

    #合并ts文件为mp3文件
    #由于广告视频没有加密，故解密时候会报错，捕获异常不让报错，解密后的广告0kb，不影响合并
    download_path = r"C:\Users\yezhoubing\Desktop\python\video\咒术回战（dec_ts）"
    hebing_path = r"C:\Users\yezhoubing\Desktop\python\video\咒术回战1.mp4"
    merge_ts(download_path, hebing_path)


if __name__ == '__main__':
    baseurl="https://www.yunb.tv/vodplay/zhoushuhuizhan-1-1.html"
    main(baseurl)
    print("all over")



