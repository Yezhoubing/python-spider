# -*- coding:utf-8 -*-
# @author:Ye Zhoubing
# @datetime:2023/7/30 19:30
# @software: PyCharm
"""
多线程下载图片
"""
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import os
import threading
# 定义一个全局锁
lock = threading.Lock()


def download_image(img_url, filename):
    response = requests.get(img_url)
    with lock: # 加锁，避免出现多个线程同时写入文件的情况，导致文件内容混乱
        if response.status_code == 200:
            print(f"Downloading {filename}")
            with open(filename, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to download {filename}")


def main():
    url = 'https://wallhaven.cc/search?q=id%3A37&sorting=random&ref=fp&seed=maYa2o&page=2'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 创建目录保存图片
    os.makedirs('./壁纸', exist_ok=True)

    images = soup.find_all('img')
    count = 1
    image_urls = []
    for image in images[1:]:
        # 根据实际情况调整
        img_url = image['data-src']
        if not img_url.startswith('https'):
            continue
        filename = f'./壁纸/{count}.jpg'
        image_urls.append((img_url, filename))
        count += 1

    max_workers = 10
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for img_url, filename in image_urls:
            future = executor.submit(download_image, img_url, filename)
            futures.append(future)

        for future in futures:
            future.result()

    print('Finished downloading picture images')


if __name__ == '__main__':
    main()