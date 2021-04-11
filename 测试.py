"""
从酷狗音乐下载试听歌曲
"""

from selenium.webdriver import Chrome
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import urllib.request

url="https://www.kugou.com/"

web=Chrome()
web.get(url)

key=input("please input your favorite song:")
time.sleep(3)

#按想要的歌曲搜索
web.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[1]/input').send_keys(key,Keys.ENTER)

time.sleep(2)
#播放搜到的第一首歌
web.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/ul[2]/li[1]/div[1]/a').click() #这里的id是动态生成
time.sleep(1)

# 转到第二个页面
web.switch_to.window(web.window_handles[-1])
web.find_element_by_xpath('/html/body/div[3]/div/table/tbody/tr[1]/td/button').click()

#拿到浏览器动态生成的html
resp_text=web.page_source

#用bs4拿到歌曲链接并下载
soup=BeautifulSoup(resp_text,"lxml")
url=soup.find("audio",class_="music").get("src")
name=soup.find("span",class_="audioName").text

#保存到本地
urllib.request.urlretrieve(url,f"{name}.mp3")

print("over")