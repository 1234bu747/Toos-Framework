# -*-coding:utf-8 -*-
import telnetlib
import time

OK = 0
FAIL = -1


class PduContrl:
    def __init__(self):
        self.host = "192.246.214.55"
        self.port = 22
        self.username = "admin"
        self.password = "admin"
        self.pdu_num = 23

    def GetPduStatus(self):
        # python2
        """
        # @Method: TelnetExecuteOperInMdc
        # @Param: 获取特定pdu口状态
        # @return: ON OFF
        """
        tn = telnetlib.Telnet(self.host, self.port)
        tn.write("\n")
        time.sleep(2)
        tn.write(self.username + "\n")
        time.sleep(2)
        tn.write(self.password + "\n")
        time.sleep(2)
        tn.write('get OutletSwitch.' + str(self.pdu_num) + "\n")
        time.sleep(2)
        tn.write("pwd\n")
        result = tn.read_until("pwd", 3)
        result1 = str(result).split("get OutletSwitch." + str(self.pdu_num))[1].split("pwd")[0]
        result0 = result1.replace("\r\n", "").split("[pdu]")[0]
        if "ON" in result0 or "on" in result0:
            return "ON"
        elif "OFF" in result0 or "off" in result0:
            return "OFF"
        else:
            return result0

    def GetPduStatus1(self):
        # python3
        """
        # @Method: TelnetExecuteOperInMdc
        # @Param: 获取特定pdu口状态
        # @return: ON OFF
        """
        tn = telnetlib.Telnet(self.host, self.port)
        tn.write(b"\n")
        time.sleep(2)
        tn.write(self.username.encode('ascii') + b"\n")
        time.sleep(2)
        tn.write(self.password.encode('ascii') + b"\n")
        time.sleep(2)
        tn.write(('get OutletSwitch.' + str(self.pdu_num)).encode('ascii') + b"\n")
        time.sleep(2)
        tn.write(b"pwd\n")
        result = tn.read_until(b"pwd", 3)
        result1 = str(result).split("get OutletSwitch." + str(self.pdu_num))[1].split("pwd")[0]
        result0 = result1.replace("\r\n", "").split("[pdu]")[0]
        if "ON" in result0 or "on" in result0:
            return "ON"
        elif "OFF" in result0 or "off" in result0:
            return "OFF"
        else:
            return result0
