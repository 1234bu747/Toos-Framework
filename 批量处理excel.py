import pandas
import os
import re

script_path = r"D:\script"
excel_path = r"D:\script\excel.xlsx"
path = []
excel = pandas.read_excel(excel_path).values.tolist()
for iterm in os.listdir(script_path):
    if "script" in iterm:
        print(iterm)
        path.append(os.path.join(script_path, iterm, "test_script.py"))
print(len(excel))
print(path)
script_path1 = r"D:＼C_have_DTC"  # 待修改脚本路径
excel_path1 = r"D:＼C_have_DTC\eventID and DTC.xlsx"  # 变量存放的excel
path1 = []
excel = pandas.read_excel(excel_path).values.tolist()  # 读取excel内容
for item in os.listdir(script_path):
    if "SYSIT_Platform_CA_DTC_Maint" in item:  # 取包含关键词的文件夹
        print(item)
        path1.append(os.path.join(script_path, item, "test_script.py"))  # 拼接文件路径和文件名为新变量并放入path列表
print(len(excel))
for i in range(len(excel)):
    with open(path[i], "r", encoding="utf-8") as file:  # 将path[i]中文件打开
        content = file.read()
        content = re.sub(r"event = [0-9]{3,5}", "event = %d" % int(excel[i][1]), content)
        # 将event=excel[i][1])数据替换原本正则匹配的event=[0-9]{3,5}数据
        # content=re.sub(r"A11654","%s" %excel[i][0],content)
        content = re.sub(r"DTC = '.+?'", "DTC = '%s'" % excel[i][0], content)
        # 懒惰模式，“.+?”为匹配任意数量的重复，但是在能使整个匹配成功的前提下使用最少的重复
        # content=re.sub(r"test_case[0-9]{3}",＂test_case%d"%int(excel[i]［2]),content)
        with open(path[i], "w", encoding="utf-8") as file2:
            # 将上述替换好的content写入path[i], 注：先以另一文件打开
            file2.write(content)
