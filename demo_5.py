# -*- codeing=utf-8 -*-
# @Time:2021/1/24 15:25
# @Author:Ye Zhoubing
# @File: demo_5.py
# @software:PyCharm
f=open("gushi.txt","w")
f.write("春眠不觉晓\n")
f.write("处处闻啼鸟\n")
f.write("夜来风雨声\n")
f.write("花落知多少\n")
f.close()
def Read():
    f1=open("gushi.txt","r")
    f2 = open("copy.txt", "w")
    contents=f1.readlines()
    i=1
    for content in contents:
        print(content,end="")
        f2.write(content)
    f1.close()
    f2.close()
    print("Successful")
if __name__ == '__main__':
    Read()

