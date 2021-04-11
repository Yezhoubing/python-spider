# 爬取酷狗音乐前500歌曲
import datetime
import time
from bs4 import BeautifulSoup
import requests
headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
def get_into(url):
    wb_data=requests.get(url,headers=headers)
    soup=BeautifulSoup(wb_data.text,'lxml')
    titles = soup.select('div.pc_temp_songlist>ul>li>a')
    ranks=soup.select('span.pc_temp_num')
    times=soup.select('span.pc_temp_tips_r>span')
    # python:
    # for in zip() 并行遍历
    for rank,title,time in zip(ranks,titles,times):
        data={
            'rank':rank.get_text().strip(),
            # Python中的strip()方法用于移除字符串指定的字符或字符序列，默认为空格或换行符，只能删除开头和结尾
            'singer':title.get_text().split('-')[0],
            # Python split()通过指定分隔符对字符串进行切片，如果参数num有指定值，则分隔num + 1个子字符串，num默认为-1，即分隔所有
            'song':title.get_text().split('-')[1],
            'time':time.get_text().strip(),
        }
        print(data)
        # 将爬取的数据存在kuhou_song.txt中
        file = open('kugou_song.txt', 'a', encoding='utf-8')
        file.write(str(data)+'\n')
        file.close()

def dat_time():
    # 获取时间并保存在txt中
    today = datetime.date.today()
    file = open('kugou_song.txt', 'a',encoding='utf-8')
    file.write('today'+' ' + 'is' + ':'+str(today)+'\n')
    file.close()
if __name__ == '__main__':
    dat_time()
#     __name__就是标识模块的名字的一个系统变量。这里分两种情况：假如当前模块是主模块（也就是调用其他模块的模块），那么此模块名字就是__main__，通过if判断这样就可以执行“__mian__:”后面的主函数内容；假如此模块是被import的，则此模块名字为文件名字（不加后面的.py），通过if判断这样就会跳过“__mian__:”后面的内容。
    urls=["https://www.kugou.com/yy/rank/home/{}-8888.html".format(str(i)) for i in range(1,24)]
    for url in urls:
        get_into(url)
        time.sleep(1)
