# -*- codeing=utf-8 -*-
# @Time:2021/3/27 16:23
# @Author:Ye Zhoubing
# @File: 多线程.py
# @software:PyCharm
#使用thread多线程
from threading import Thread  #线程类
# def func():
#     for i in range(0,1000):
#         print("children",i)
#     return 0
#
#
# if __name__ == '__main__':
#     t=Thread(target=func) #创建一个多线程运行func（），传参可通过元组或字典
#     t.start()  #多线程可以开始运行，运行时间取决于cpu
#     for i in range(0,1000):
#         print("father",i)

#第二种写法
class MyThread(Thread): #继承类
    def run(self):   #重写run()，当线程被执行时，执行的就是run（）
        for i in range(0, 1000):
            print("children",i)

if __name__ == '__main__':
    t=MyThread() #创建一个多线程运行func（），传参可通过元组或字典
    t.start()  #多线程可以开始运行，运行时间取决于cpu
    for i in range(0,1000):
        print("father",i)


