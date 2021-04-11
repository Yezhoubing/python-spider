# -*- codeing=utf-8 -*-
# @Time:2021/3/26 9:06
# @Author:Ye Zhoubing
# @File: 代理ip.py
# @software:PyCharm

#使用代理ip防止被ban



import requests
url="https://www.baidu.com"
proxies={
#https://www.zdaye.com/FreeIPList.html在该网址找代理IP，推荐使用透明状态
#此时网站遵循https协议，3128是端口;http网址则用http
    "http":"http://218.75.102.198:8000",
    "https":"https://218.75.102.198:8000"
}

resp=requests.get(url)
resp.encoding="utf-8"
print(resp.text)