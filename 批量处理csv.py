import pandas
import os
import re
import csv

j = 1
script_path = r"D:\script"
excel_path = r"D:\script\excel.csv"
fail_list = []
with open(excel_path) as f:
    excel = csv.DictReader(f)
    for i in excel:
        print(i["DTC"])


def test_case01(self, setup):
    j = 1
    excel_path = r"/home/C.csv"  # 变量存放的excel
    Failed_list = []
    with open(excel_path) as f:
        excel = csv.DictReader(f)
        for i in excel:
            case_name ="SYSIT_Platform_CA_DTC_Case_00{}".format(j)
            print(i)
            DTC = i["DTC"]
            eventID = int(i["eventID"])
            SERVER_IP = '192.246.214.55'
            result = self.DTC_CommonApi.creat_fault_read_DTC(eventID, DTC, SERVER_IP)
