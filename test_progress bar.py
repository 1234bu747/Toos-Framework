# -*-coding:utf-8 -*-
# 编码格式

# 导入库
import time
import yaml
import json
import pandas
import paramiko
import xlrd
import xlwt
import re
import os
import sys
import pyshark
import shutil
import scapy
import scrapy
import doipclient
import pytest
import requests
import selenium
from lib.DiCommonApi import *

# 添加绝对路径
sys.path.append(os.path.dirname((os.path.realpath((__file__)).lower().split("testscript")[0])))
sys.path.append(os.path.abspath('.').split("SYSIT")[0] + "SYSIT/scripts")
# 导入公共函数


class TestClass:
    @pytest.fixture(scope="function")
    def setup(self, request):
        self.Preconditin()
        def teardown(self):
            self.Postcondition()
            print("teardown is called\n")
            request.addfinalizer(teardown)
            print("setup is clled\n")

    def Precondition(self):
        # 加载配置文件的参数
        configFile = os.path.abspath(os.path.dirname(__file__)) + "/config.json"
        with open(configFile, "r") as jsonfile:
            config = json.load(jsonfile)
            self.GetParameter(config['specialInfo'])
        # 初始化路径
        env_array = os.environ
        self.outdir = env_array["CASETEST_OUTPUT_DIR"]
        self.dele_node = config["specialInfo"]["node_deleted"]
        # PrintStepname("1.获取全局变量")
        # 初始化公共API
        self.diCommAPI = DiCommonApi()
        return

    def Postcondition(self):
        # =======关闭终端======
        self.diCommAPI.CommonApi_clearEnv()
        # cmd = "rosparam set"
        # retstr = self.runCmd(cmd)
        # =======测试环境恢复结束========
        print("teardown is called")
        return

    def runCmd(self, cmd):
        output = os.popen(cmd)
        retstr = output.read()
        return retstr

    def test_case001(self):
        print("脚本编写区域")
        print("执行进度条显示")
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





    def GetParameter(self, item):
        for key in item:
            # if "" != item[key] or None != item[key]:
            print("key:", key)
            print("value:", item[key])
        vars(self)[key] = item[key]
        # self.env.list_all_member()
        return

    def CheckResult(self, result, expected_result=None):
        # 断言
        assert result == expected_result
        return

    def check_process(self, process_name):
        cmd = 'ps -ef|grep -w"' + process_name + '"|grep -v .sh|grep -v grep'
        print("cmd:====" + cmd)
        isok = self.diCommAPI.CommonApi_ExecuteOperInMdc(cmd)
        print("isok:", isok)
        isok = isok.split("\n")
        del isok[-1]
        return len(isok)
