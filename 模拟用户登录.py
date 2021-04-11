# -*- codeing=utf-8 -*-
# @Time:2021/3/24 20:06
# @Author:Ye Zhoubing
# @File: 模拟用户登录.py
# @software:PyCharm
#利用cookie模拟用户登录17k小说网
import requests

#session 会话  发出一连串的请求，过程中cookie不会丢失
session=requests.session()

#用户登录
#信息在登录界面出现的login日志中
request_url="https://passport.17k.com/ck/user/login"
data={
    "loginName": "15850657813",
    "password": "ab0011"
}
resp_1=session.post(request_url,data=data)

print(resp_1.cookies) #看cookie

#抓取书架上的书
#在xhr中找到包含有书的链接，因为是动态变化，源网页没有
#session中才有cookie
# resp_2=session.get("https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919")

#这种写法比较麻烦
headers={
"Cookie": "GUID=1153c605-b6e8-4cbf-abd7-7cb89aaec5e3; sajssdk_2015_cross_new_user=1; c_channel=0; c_csc=web; accessToken=avatarUrl%3Dhttps%253A%252F%252Fcdn.static.17k.com%252Fuser%252Favatar%252F08%252F88%252F03%252F76410388.jpg-88x88%253Fv%253D1616588466000%26id%3D76410388%26nickname%3D%25E5%25AE%2589%25E4%25B9%2589124%26e%3D1632141113%26s%3D55e435b60602c492; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2276410388%22%2C%22%24device_id%22%3A%22178642c538337f-02fd5ca7359933-5771031-1327104-178642c538441d%22%2C%22props%22%3A%7B%7D%2C%22first_id%22%3A%221153c605-b6e8-4cbf-abd7-7cb89aaec5e3%22%7D; Hm_lvt_9793f42b498361373512340937deb2a0=1616589122; Hm_lpvt_9793f42b498361373512340937deb2a0=1616589122"
}
resp_2=requests.get("https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919",headers=headers)
content=resp_2.json()
print(content)
