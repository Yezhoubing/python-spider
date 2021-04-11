# -*- codeing=utf-8 -*-
# @Time:2021/3/24 16:19
# @Author:Ye Zhoubing
# @File: 猪八戒网.py
# @software:PyCharm

import requests
from lxml import etree

#爬取猪八戒网南京商标logo设计公司
def main():
    url="https://nanjing.zbj.com/logo/f.html?fr=newpdy.ppsj.20.5.27"
    resp=requests.get(url)
    content=resp.text
    # print(content)
    tree=etree.HTML(content) #这里用html解析

    #绝对路径只要有一个元素变化就爬不到数据
    # divs=tree.xpath("/html/body/div[6]/div/div/div[6]/div[3]/div[1]/div/div")

    #相对路径，这里定位到class='witkey-item grid-box'的div标签
    divs=tree.xpath("//div[@class='witkey-item grid-box']")
    # print(divs)
    for div in divs:

        name=div.xpath("./div[1]/div[2]/section[1]/h4/a/text()")
        price=div.xpath("./div[2]/div[2]/i/text()")[0].strip("¥")

        # Python join() 方法用于将序列中的元素以指定的字符连接生成一个新的字符串。
        introduction="logo".join(div.xpath("./div[2]/div[3]/a/text()"))



        print(introduction)


if __name__ == '__main__':
    main()