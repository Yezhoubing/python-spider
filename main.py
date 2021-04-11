# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
L2 = {'1':'A','2':'B','3':'C','4':'D'}
L3 = {'5':'a','6':'b','7':'c','8':'d'}
blist = []
for m,n in zip(L2.values(),L3.values()):
  blist.append(m)
  blist.append(n)
print('字典L1：', L2)
print('字典L2：', L3)
print('字典L1的值对应字典L2的值输出：',blist)