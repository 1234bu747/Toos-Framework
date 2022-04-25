# -*-coding:utf-8 -*-
import pyshark

cap = pyshark.FileCapture('uss2.cap')
for packet in cap:
    print(packet)
    try:
        print("packet.layers[3].Payload", packet.layers[3].Payload)  # 读取Layer SOMEIP的Payload
    except:
        pass
cap.close()  # 关闭文件读取
