# -*- codeing=utf-8 -*-
# @Time:2021/3/30 16:15
# @Author:Ye Zhoubing
# @File: 线程池爬取菜价.py
# @software:PyCharm
#利用进程与线程爬取北京新发地菜价表格数据
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import xlwt #将数据存为excel文件


def main(url):

        resp = requests.get(url)
        content=resp.text

        # 浏览器会在table中加上tbody，实际源代码没有该标签
        html = etree.HTML(content)
        # 爬取位置从2开始的tr
        # trs = html.xpath("/html/body/div[2]/div[4]/div[1]/table/tr[position()>1]")
        trs = html.xpath("/html/body/div[2]/div[4]/div[1]/table/tr")[1:]


        for tr in trs:
            tds=tr.xpath("./td/text()")

            #list() 方法用于将元组转换为列表#第二个item将数据中的数组元素进行迭代，以列表的形式返回放在第一个item里面,再将\\  /  |替换掉
            # tds=list((item.replace("\\","_").replace("/", "_").replace("|"," ") for item in tds))
            #下面这种与上面的相同
            tds=[item.replace("\\","_").replace("/", "_").replace("|"," ") for item in tds]
            datalist.append(tds)



        print(url,"over")









if __name__ == '__main__':
    datalist=[]
    # 将数据存为北京新发地菜价.xls
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet("mysheet", cell_overwrite_ok=True)
    title = ["品名", "最低价", "平均价", "最高价", "规格", "单位", "发布日期"]
    for i in range(0, 7):
        worksheet.write(0, i, title[i])
    with ThreadPoolExecutor(50) as t:
        for i in range(1, 200):
            url = f"http://www.xinfadi.com.cn/marketanalysis/0/list/{i}.shtml"
            t.submit(main,url)

    for i in range(0, 7):
        worksheet.write(0, i, title[i])

    for j in range(1, len(datalist)+1):
        data = datalist[j - 1]
        for i in range(0, 7):
            worksheet.write(j, i, data[i])

    workbook.save("北京新发地菜价.xls")




    print("over")

