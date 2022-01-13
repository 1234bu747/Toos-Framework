# -*-coding:utf-8 -*-
import time

scale = ["*"] * 50  # 总量，和第一个类似
# print("执行开始".center(len(scale)//2,"-"))#产生这个-----------执行开始----------
t = time.perf_counter()
for i in range(len(scale) + 1):  # 50不能打印出来，要加+1
    a = "*" * i
    b = "'" * (len(scale) - i)
    c = (i / len(scale)) * 100  # 百分比进度 50%那种
    t = time.perf_counter()  # 消耗时间
    print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c, a, b, t), end="")  # 总的进度条，和第二种类型
    time.sleep(0.1)
print("\n" + "执行结束".center(len(scale) // 2, "-"))
