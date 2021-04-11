# -*- codeing=utf-8 -*-
# @Time:2021/1/20 13:19
# @Author:Ye Zhoubing
# @File: demo_4.py
# @software:PyCharm
products=[["iphone",6888],["MacPro",14800],["小米6",2499],["Coffee",31],["Book",60],["Nike",699]]
print("-"*6+"  商品列表   "+"-"*6)
for i in range(0,len(products)):
    j=0
    print(i,end="\t")
    print(products[i][j],end="\t")
    print(products[i][j+1],end="\t")
    print(end="\n")

my_products=[]
while True:
    num=input("select your favorite products:")
    if num=="q":
        for my_product in my_products:
            print(my_product)
        break
    else:
        i=int(num)
        my_products.append(products[i])


