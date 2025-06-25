# -*- coding: utf-8 -*-

import os

data = read_File_Data()
# 读取ini文件
# iniPath = os.path.join(baseDir, 'config', 'setting.ini')
# url = data.load_ini(iniPath)
csvPath = os.path.join(baseDir, 'Https.csv')
print(csvPath)
# headers = data.read_csv

"""
payload = {'pageNum': '1',
'pageSize': '10',
'mobile': '18039537200'}

headers = {
  'Authentication-Admin-Web-Token': '91a3763b8eb940a0bed7bbae7e3e01f5'
}

response = requests.request("GET", url, headers=headers, params=payload)

print(response.json())
"""