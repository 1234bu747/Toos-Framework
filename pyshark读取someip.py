# -*-coding:utf-8-*-
from scapy.all import *
import sys
import os
import socket
import struct
import pyshark

# wireshark软件，someip报文解析自动化
# 打开存储的捕获文件
capfile = "C:/User/uss2.cap"  # 捕获的报文(文件名+路径)
cap = pyshark.FileCapture(capfile)
# for pkt in cap:
# print(pkt.sniff_time)
cap = pyshark.FileCapture(capfile, display_filter='someip.serviceid' == 0x750)
print(cap)
for pkt in cap:
    print("pkt:", pkt)
    print("pkt.sniff_time:", pkt.sniff_time)  # 报文捕获时间(毫秒级)
    print("pkt.sniff_timestamp:", pkt.sniff_timestamp)  # 报文捕获时间(纳秒级)
    print("pkt.highest_layer:", pkt.highest_layer)  # 过滤后的报文头
    print("pkt.layers[3].Payload:", pkt.layers[3].Payload)
    Someip = pkt.layers[3].Payload
    someip_id = Someip[-2:]  # 取someip最后两位
