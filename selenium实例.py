# 打开python官网，并在搜索框内搜索python
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver=webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chromedriver.exe')#输入webdriver路径
driver.get('http://www.python.org')#driver.get方式与requests.get类似
assert "Python" in driver.title#查看网页标题是否是python
elem=driver.find_element_by_name('q')#找到name=‘q’的输入框
elem.clear()#清空输入框
elem.send_keys("python")#在输入框中输入python
elem.send_keys(Keys.RETURN)#按回车发送，模拟键盘Enter键提交搜索需求
time.sleep(10)#延迟10s后关闭窗口
driver.close()
driver.find_element_by_xpath()