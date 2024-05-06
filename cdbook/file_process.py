# -*- coding:utf-8 -*-
# @author:Ye Zhoubing
# @datetime:2024/5/6 9:08
# @software: PyCharm
"""
自动批量整理文件夹下文件
todo:如果目标目录下有文件夹就会报错
"""
import os
import re
import shutil
from collections import defaultdict


def organize_files(source_dir):
  # 检查源目录
  if not os.path.exists(source_dir):
    print("源目录不存在!")
    return

  # 获取源文件列表
  files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir,f))]  # 排除文件夹的影响

  # 使用正则提取文件名信息
  p = re.compile(r'(.*?)(\d+)?\..*')  # 匹配文件名和数字，第一个为文件名，第二个为数字
  groups = defaultdict(list)

  for file in files:
    name = p.match(file).group(1)
    groups[name].append(file)

  # 移动文件
  for name, files in groups.items():
    if len(files) > 0:
      target_dir = os.path.join(source_dir, name)
      os.makedirs(target_dir, exist_ok=True)  # 如果目录不存在就创建,存在就忽略

      for file in files:
        source = os.path.join(source_dir, file)
        target = os.path.join(target_dir, file)
        shutil.move(source, target)
        print(f"移动,{file}成功")

  print("文件整理完成!")


if __name__ == '__main__':
  source_dir = input("源目录:")
  organize_files(source_dir)