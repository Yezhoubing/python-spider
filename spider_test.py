import requests
url="http://www.baidu.com"
html=requests.get(url)
print(html.text)