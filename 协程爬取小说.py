# -*- codeing=utf-8 -*-
# @Time:2021/3/31 18:37
# @Author:Ye Zhoubing
# @File: 协程爬取小说.py
# @software:PyCharm

# 小说页面http://dushu.baidu.com/pc/detail?gid=4306063500

#目录发出请求的网址http://dushu.baidu.com/api/pc/getCatalog?data={%22book_id%22:%224306063500%22}，得到目录标题及对应的cid
#章节内容http://dushu.baidu.com/api/pc/getChapterContent?data={%22book_id%22:%224306063500%22,%22cid%22:%224306063500|11348571%22,%22need_bookinfo%22:1}

#%22改为引号，包裹的内容是参数

import requests
import asyncio
import aiohttp
import json
import aiofiles #异步操作文件


async def Get_catalog(url):
    resp = requests.get(url)
    dic = resp.json()
    tasks = []

    print(dic)
    for item in dic["data"]["novel"]["items"]:
        title = item["title"]
        cid = item["cid"]

        tasks.append(asyncio.create_task(aiodowload(cid, title, b_id)))
        await asyncio.wait(tasks)
        # print(title,cid)


async def aiodowload(cid, title, b_id):
    data={
        "book_id": b_id,
        "cid": f"{b_id} | {cid}",
        "need_bookinfo" : 1
    }

    content_data=json.dumps(data) #json.dumps 用于将 Python 对象编码成 JSON 字符串。
    url=f"http://dushu.baidu.com/api/pc/getChapterContent?data={content_data}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            dic=await resp.json() #转换为json文件
            # print(dic["data"]["novel"]["content"])

            #用aiofiles存储文件
            async with aiofiles.open(f"novel/{title}.txt",mode="w",encoding="utf-8") as fp:
                await fp.write(dic["data"]["novel"]["content"])

    print(title,"over")





if __name__ == '__main__':
    b_id="4306063500"
    catalog_url = f'http://dushu.baidu.com/api/pc/getCatalog?data={{"book_id":{b_id}}}'#book_id:用{{}}，表示不作变量使用
    asyncio.run(Get_catalog(catalog_url))

