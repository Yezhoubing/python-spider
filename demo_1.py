import random

a = input("请输入：剪刀（0）、石头（1）、布（2）：")  # a为输入值

if a == 0:
    print("您的输入为:剪刀（0）")
elif a == 1:
    print("您的输入为:石头（1）")
elif a == 2:
    print("您的输入为:布（2）")
b = random.randint(0, 2)  # b为随机生成数字，0、1、2
print("随机生成的数字是：%d" % b)
if int(a) > b or (int(a)==0 and b==2):
    print("恭喜你，你赢了")
else:
    print("哈哈，你输了")
