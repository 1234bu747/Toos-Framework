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


class DiCommonApi:
    def __init__(self):
        self.host = "192.246.214.55"
        self.port = 22
        self.username = "root"
        self.password = "root"
        env_array = os.environ
        self.mdcUser = env_array['USER']
        self.mdclp = env_array['IP']
        self.mdcPass = env_array['PASS']  # 传参

    def CommonApi_ExecuteOperInMdc(self, cmd="pwd"):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.host, port=self.port, username=self.username, password=self.password)
        cmd = "source /etc/profile;" + cmd
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read().decode()  # unicode转字符-py3
        ssh.close()
        return result

    # def CommonApi_CopyFileFromMdc(self, host="192.246.214.55", cmd="pwd"):
    #     getfile = f"sshpass -p {self.password} scp -P {self.port} -o UserKnownHostsFile="
