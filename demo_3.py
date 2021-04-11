# -*- codeing=utf-8 -*-
# @Time:2021/1/13 19:04
# @Author:Ye Zhoubing
# @File: demo_3.py
# @software:PyCharm
for i in range(1,10):
    n=1
    while n<i or n==i:
        r=i*n
        print("%d*%d=%d"%(i,n,r),end="\t")
        n+=1
    print(end="\n")

