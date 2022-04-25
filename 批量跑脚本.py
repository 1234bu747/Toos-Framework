# -*-coding:utf-8 -*-
import os
import time

list = []
Dir = os.path.abspath(os.path.dirname(__file__))  # 脚本的路径
f = os.popen("ls")  # 列出工作站当前路径下所有文件夹
a = f.read().splitlines()
print(a, Dir)
for i in a:
    if "SWscript" in i:
        list.append(i)
print(list)
for i in range(len(list)):
    cmd1 = "pytest -s " + Dir + "/" + list[i] + "/test_script.py "
    print(cmd1)
    aaa = os.popen(cmd1).read()  # 工作站运行cmd1并回显结果
    print("testcase:", aaa)
    if ("failed," not in aaa) and ("passed, " in aaa):
        f = open("/home/result.txt", "a+")
        f.write(list[i] + " success＼n")
        f.close()
    else:
        f = open("/home/result.txt", "a+")
        f.write(list[i] + " failed＼n")
        f.close()
# 这是把文件夹内所有脚本串起来跑的脚本，并且会把跑的结果写到rusult.txt里面
