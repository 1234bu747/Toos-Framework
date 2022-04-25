# -*-coding:utf-8 -*-
import secrets
from scapy.all import *


def gen_check_sum(old_checksum):
    print("secrets.token_hex(2):", secrets.token_hex(2))  # 传随机的如f5b3参数
    new_checksum = int('Ox' + secrets.token_hex(2), 16)  # 转10进制
    if new_checksum == old_checksum:
        gen_check_sum(old_checksum)
    else:
        pass
    return new_checksum


pkts = []
count = 0
for pkt in rdpcap('1111.pcap'):
    count += 1
    result = hexdump(pkt['Raw'], dump=True)  # 转pkt['Raw']为16进制
    print(result)
    print(count)
    print(pkt.show())  # 显示全部
    print("pkt['UDP'].chksum:", pkt['UDP'].chksum)
    print("pkt['Raw']:", pkt['Raw'])
    try:
        new_checksum = gen_check_sum(pkt['UDP'].chksum)
        pkt['UDP'].chksum = new_checksum
    except IndexError:
        pass
    # break
    pkts.append(pkt)
wrpcap('2222.pcap', pkts)  # 写改完checksum值为新文件
