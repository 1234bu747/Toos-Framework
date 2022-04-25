# －*－coding:utf-8-*-
# 框架
import pytest
import os
import sys
import json
from lib import *

sys.path.append(os.path.dirname(os.path.realpath(__file__)).lower().split("testscript")[0])
sys.path.append(os.path.abspath('.').split("SYSIT")[0] + "SYSIT/scripts")


class TestClass:
    @pytest.fixture(scope="function")
    def setup(self, request):
        self.Precondition()

        def teardown():
            self.Postcondition()
            print("teardown is called\n")
            request.addfinalizer(teardown)
            print("setup is called\n")

    def Precondition(self):
        # 加载配置文件的参数
        configFile = os.path.abspath(os.path.dirname(__file__)) + "/config.json"
        with open(configFile, 'r') as jsonfile:
            config = json.load(jsonfile)
        self.GetParameter(config['speciallnfo'])
        # 初始化路径
        env_array = os.environ
        self.datadir = env_array['CASETEST_INPUT_DIR']
        self.outdir = env_array['CASETEST_OUTPUT_DIR']
        self.dele_node = config['speciallnfo']['node_deleted']
        PrintStepname("1、获取全局变量＂）
        # 初始化公共API
        self.diCommAPI = DiCommonApi()
        self.SensorCommonApi = sysit_func_SensorCommonApi()
        self.AppCommonApi = sysit_func_AppCommonApi()
        return

    def Postcondition(self):
        # 关闭终端
        self.diCommAPI.CommonApi_clearEnv()
        # cmd = "rosparamset / lidar_config"+self.lidar_config
        # retstr = self.runCmd(cmd)
        # 测试环境恢复结束
        print("teardown iscalled")
        return

    def runCmd(self, cmd):
        output = os.popen(cmd)
        retstr = output.read()
        return retstr

    def test_case1(self, setup):
        print(1)
        # 脚本编辑

    def GetParameter(self, item):
        for key in item:
            # if "" != item[key] orNone != item[key]:
            print("key:", key)
            print("value: ", item[key])
            vars(self)[key] = item[key]
            # self.env.list_all_member()
        return

    def CheckResult(self, result, expected_result=None):
        # 断言
        assert (result == expected_result)
        return

    def check_process(self, process_name):
        cmd = "ps -ef | grep -w" + process_name + "|grep －v .sh | grep - v grep"
        print("cmd:====" + cmd)
        isok = self.diCommAPI.CommonApi_ExecuteOperlnMdc(cmd)
        print("isok:", isok)
        print(isok)
        isok = isok.split("\n")
        del isok[-1]
        return len(isok)
