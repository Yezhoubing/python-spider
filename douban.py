# -*- codeing=utf-8 -*-
# @Time:2021/1/28 9:53
# @Author:Ye Zhoubing
# @File: douban.py
# @software:PyCharm
import os
import re
import shutil
import urllib.error
import sqlite3
from bs4 import BeautifulSoup
import requests
import xlwt
headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
def main():
    baseurl="https://movie.douban.com/top250?start="
    #爬取网页
    datalist=getData(baseurl)
    # savepath="豆瓣电影250.xls"
    # saveData(datalist,savepath)
    dbpath="douban.db"
    saveDataDb(datalist,dbpath)

#影片格式规则
findLink=re.compile(r'<a href="(.*?)">')#注意“（）”，如果没有（.*?）的括号，会带有a标签（影片链接）
findTitle=re.compile(r'<span class="title">(.*)</span>')#(影片片名)

#<img>不闭合，故只写一个<
findImg=re.compile(r'<img .*src="(.*?)"',re.S)#.*表示img和src中有若干个字符，re.S表示忽视换行符（影片图片）,img不要写后面的>,否则会显示图片后的内容

findScore=re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')#（影片评分）
findJudge=re.compile(r'<span>(\d*)人评价</span>')#(\d*)表示多个数字(评分人数)
findSentence=re.compile(r'<span class="inq">(.*)</span>')#(一句话简介)
findBd=re.compile(r'<p class="">(.*?)</p>',re.S)#((影片相关人员内容)#爬取到的内容是class=“”，就写class=“”，不要写在浏览器中看到的class

#逐个解析数据
def getData(baseUrl):
    datalist=[]
    for i in range(0,10):#获取10个页面。共计250个
        url=baseUrl+str(i*25)
        soup=askUrl(url)#将返回的html储存在html变量中
        #逐一解析数据
        for item in soup.find_all("div",class_="item"):#查找符合要求div标签，class为item的内容，形成列表
            # print(item)#检验爬取到的电影全部信息
            data=[]
            item=str(item)

            #获取指定规则的内容
            link=re.findall(findLink,item)[0]#在item中找到对应规则的元素
            data.append(link)#添加链接
            titles=re.findall(findTitle,item)#片名不止一个
            if(len(titles)==2):
                ctitle=titles[0]
                data.append(ctitle)#添加中文标题
                otitle=titles[1].replace("\xa0/\xa0","")#将/与空格替换掉
                data.append(otitle)#添加外文标题
            else:
                data.append(titles[0])
                data.append(" ")#留空占位
            img=re.findall(findImg,item)[0]#在item中找到对应规则的元素
            data.append(img)#添加图片
            score= re.findall(findScore, item)[0]  # 在item中找到对应规则的元素
            data.append(score)  # 添加评分
            judge= re.findall(findJudge, item)[0]  # 在item中找到对应规则的元素
            data.append(judge)  #添加评分人数
            sentence= re.findall(findSentence, item)  # 在item中找到对应规则的元素（可能有的元素无该要素）
            if(len(sentence)!=0):
                sentence=sentence[0].replace("。","")#去掉“。”
                data.append(sentence)# 添加简介
            else:
                data.append(" ")#留空
            bd= re.findall(findBd, item)[0]  # 在item中找到对应规则的元素
            bd=re.sub("<br(\s+)?/>(\s+)?"," ",bd)#去掉br，\s代表正则表达式中的一个空白字符（可能是空格、制表符、其他空白），用于匹配空白字符
            data.append(bd.strip())  # 添加相关内容,去掉前后空格
            datalist.append(data)#将处理好的一部电影放入datalist
    # print(datalist)#\xa0表示空格
    return datalist


#得到一个指定的url内容
def askUrl(url):
    response=requests.get(url,headers=headers)
    try:
        soup=BeautifulSoup(response.text,'lxml')
        return soup
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)


#保存数据为excel文件
def saveData(datalist,savepath):
    print("保存中")
    workbook = xlwt.Workbook(encoding="UTF-8",style_compression=0)  # style_compression表示是否压缩，不常用。
    worksheet = workbook.add_sheet('豆瓣电影top250',cell_overwrite_ok=True)#可以重新覆盖
    col=("影片链接","影片片名（中）","影片片名（外）","影片图片","影片评分","评分人数","一句话简介","影片相关人员内容")
    for i in range(0,8):
        worksheet.write(0,i,col[i])  #往第0行第i列写col[i],从左上0开始
    for i in range(0,250):
        print("第%d部电影完成"%(i+1))
        data=datalist[i]
        for j in range(0,8):
            worksheet.write(i+1,j,data[j])
    workbook.save(savepath)  # 保存整个文件为xls，xlwt模块不支持xlsx格式，此时文件不应该正在被打开占用，否则保存失败
    aa = os.getcwd()

    # 获取当前文件路径
    file_path = os.path.join(aa, savepath)

    # 移动文件到E盘地方
    target_path = r"C:\Users\yezhoubing\Desktop"#将保存的文件移动在绝对路径桌面上，文件名为豆瓣电影250.xls
    # 使用shutil包的move方法移动文件
    shutil.move(file_path, target_path)

def saveDataDb(datalist,dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index==4 or index==5:#评分与评分人数是数字，不加双引号
                continue
            data[index]='"'+data[index]+'"'
        #注意是values
        sql='''
            insert into douban_250(
            src_link,cname,ename,img_link,score,judge,sentence,db
            )
            values(%s)
        '''%",".join(data)#data中每个元素插入一个“，”
        # print(sql)
        c.execute(sql)
        conn.commit()
    conn.close()

    print("保存至数据库douban.db")


def init_db(dbpath):
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()  # 获取游标

    sql = '''
    create table douban_250(
    id integer primary key autoincrement,
    src_link text,
    cname varchar ,
    ename varchar ,
    img_link text,
    score numeric ,
    judge numeric ,
    sentence text,
    db text
    )
    '''

    cursor = c.execute(sql)  # 执行sql语句,用cursor接收返回值
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
    print("保存完成")