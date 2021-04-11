import jieba#用于分词
from matplotlib import pyplot as plt#绘图，数据可视化
from wordcloud import WordCloud#词云,注意大小写
from PIL import Image#用于图形处理
import numpy as np#用于矩阵运算
import sqlite3

#准备词云所需的文字
con=sqlite3.connect("douban.db")
cur=con.cursor()
sql="select sentence from douban_250"
data=cur.execute(sql)
text=""
for item in data:
    text=text+item[0]
cur.close()
con.close()

#分词
cut=jieba.cut(text)
string=" ".join(cut)
# print(string)

#生成遮罩图片
img=Image.open(r'C:\Users\yezhoubing\Desktop\前端素材\tree.jpg')#打开遮罩图片
img_array=np.array(img)#将图片转换成数组（图片背景要纯净）
wc=WordCloud(
    # 这是输出的设置
    background_color="#99FFFF",
    mask=img_array,
    font_path="simkai.ttf"#注意字体中英文
)
wc.generate_from_text(string)

#绘制图片
fig=plt.figure(1)#创建第一个图像，新建一个名叫 Figure1的画图窗口
plt.imshow(wc)#用wc规则显示
plt.axis("off")#是否显示坐标轴

# plt.show()#显示生成的词云图片，在Plots窗口中

#输出词云图片到文件
plt.savefig(r'C:\Users\yezhoubing\Desktop\前端素材\tree_word.jpg',dpi=600)#保存为tree_word.jpg，分辨率dpi默认为400

