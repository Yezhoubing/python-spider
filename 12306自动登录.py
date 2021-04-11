# -*- codeing=utf-8 -*-
# @Time:2021/4/5 14:20
# @Author:Ye Zhoubing
# @File: 12306自动登录.py
# @software:PyCharm
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from chaojiying import Chaojiying_Client
from selenium.webdriver.chrome.options import Options
import time
#防止被检测出来是自动软件
option = Options()
option.add_experimental_option('excludeSwitches',
['enable-automation'])
option.add_argument('--disable-blink-features=AutomationControlled')
web = Chrome(options=option)
web.get('https://kyfw.12306.cn/otn/resources/login.html')

time.sleep(3)

#转到账号登录
web.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[2]/a').click()

#输入账号密码，假设账号为123，密码为123456
web.find_element_by_xpath('//*[@id="J-userName"]').send_keys('123')
web.find_element_by_xpath('//*[@id="J-password"]').send_keys('123456')

    #输入验证码
verify_img=web.find_element_by_xpath('//*[@id="J-loginImg"]')
chaojiying = Chaojiying_Client('15850657813', 'yzb20001123', '96001')
result=chaojiying.PostPic(verify_img.screenshot_as_png, 9004) #选择坐标多选,返回1~4个坐标,如:x1,y1|x2,y2|x3,y3
#将其中的坐标提取出来
P_list=result['pic_str'].split('|')
for P in P_list:
    P_x=int(P.split(',')[0])
    P_y=int(P.split(',')[1])
    #.perform()表示执行ActionChains行为,.click()先点击坐标位置再执行
    ActionChains(web).move_to_element_with_offset(verify_img,P_x,P_y).click().perform()

time.sleep(3)
#点击立即登录
web.find_element_by_xpath('//*[@id="J-login"]').click()

time.sleep(5) #等待缓冲出滑块

#将滑条移到最右端
btn=web.find_element_by_xpath('//*[@id="nc_1_n1z"]')
ActionChains(web).drag_and_drop_by_offset(btn,370,0).perform() #单位为px，顺序为x，y
