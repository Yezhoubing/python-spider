# -*- codeing=utf-8 -*-
# @Time:2021/3/30 20:16
# @Author:Ye Zhoubing
# @File: aiohttp使用爬取图片.py
# @software:PyCharm
import aiohttp
import asyncio
# text() 返回字符串数据

# read() 返回二进制数据

# json() 返回json对象
async def  Dowload(url,x):
    name = "欧根"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            with open(f"{name}{x}.png",mode="wb") as f:
                f.write(await resp.content.read())
                x=x+1
            # resp.content.read() #等价于resp.content

            # b=resp.text() #等价于resp.text
            # print(b)
            # # resp.json() #等价于resp.json

        # session.get()
        # session.post()

    # s=aiohttp.ClientSession() #相当于requests
    # s.get()   #相当于requests.get(),post()同理
    # print()
    print(name,"over")

async def main():
    x=0
    url_list=[
        "http://fleet.diablohu.com/!/pics-ships//176/8.png",
        "http://fleet.diablohu.com/!/pics-ships//176/9.png",
        "http://fleet.diablohu.com/!/pics-ships//177/8.png",
        "http://fleet.diablohu.com/!/pics-ships//177/9.png"
    ]
    tasks=[]
    for url in url_list:
        x=x+1
        img=asyncio.create_task(Dowload(url,x))
        tasks.append(img)

    await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())
