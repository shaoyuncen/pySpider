# -*- coding: utf-8 -*-

# 通过http请求一次性获取苏州市采购网的招标信息的所有url

import requests
import json
import time

post_parameters = {
    'type' : '',
    'title' : '',
    'choose' : '',
    'projectType' : '',
    'zbCode' : '',
    'appcode' : '',
    'page' : '',
    'rows' : '5'
}
cpContent = requests.post("http://www.zfcg.suzhou.gov.cn/content/cpContents.action", data = post_parameters) #POST请求
print(cpContent.status_code)
# request对象转Dict类型
jsonDict = cpContent.json()

# # 保存文件
# f = open('./jsonData.json', 'a', encoding = 'utf-8')
# f.write(json.dump(jsonDict, f, indent = 4, ensure_ascii = False))
# f.close()

# 抽取urls
urls = []
for li in jsonDict['rows']:
    urls.append("http://www.zfcg.suzhou.gov.cn/html/project/" + li['ID'] + ".shtml")

t1 = time.time()

file=open('urls.txt','w') 
urls = [line + '\n' for line in urls]
file.writelines(urls)
file.close()

t = time.time() - t1
print(t)