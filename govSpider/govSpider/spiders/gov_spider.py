# -*- coding: utf-8 -*-
import requests
import json
import time
import scrapy
from scrapy.selector import Selector
from govSpider.items import GovspiderItem

geturls = []

post_parameters = {
    'type' : '',
    'title' : '',
    'choose' : '',
    'projectType' : '',
    'zbCode' : '',
    'appcode' : '',
    'page' : '',
    'rows' : '10' # url个数，可以自己设置
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
geturls = []
for li in jsonDict['rows']:
    geturls.append("http://www.zfcg.suzhou.gov.cn/html/project/" + li['ID'] + ".shtml")

count = 0

class govSpider(scrapy.Spider):
    name = "gov"

    def start_requests(self):
        global geturls
        urls = geturls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        sel = Selector(response)

        govItem = GovspiderItem()

        # 侧边栏
        govItem['label_tender'] = "y" # 招标公告

        govItem['label_notice'] = 'y' if self.isExist(sel.xpath('//*[@id="menu"]/li[2]/a').extract_first())  else 'n'  # 补充通知
        
        govItem['label_winBid'] = 'y' if self.isExist(sel.xpath('//*[@id="menu"]/li[3]/a').extract_first())  else 'n'  # 中标公告
        
        govItem['label_purchaseFile'] = 'y' if self.isExist(sel.xpath('//*[@id="menu"]/li[4]/a').extract_first())  else 'n'  # 采购文件
        
        govItem['label_purchaseContract'] = 'y' if self.isExist(sel.xpath('//*[@id="menu"]/li[5]/a').extract_first())  else 'n'  # 采购合同
        
        govItem['label_dealContract'] = 'y' if self.isExist(sel.xpath('//*[@id="menu"]/li[6]/a').extract_first())  else 'n' # 成交公告

        # 8个标签的抽取
        govItem['proj_area'] = sel.xpath('/html/body/div[2]/div[2]/table/tr[1]/td[1]/text()').extract_first()
        # 项目地区
        govItem['proj_class'] = sel.xpath('/html/body/div[2]/div[2]/table/tr[1]/td[2]/text()').extract_first()
        # 项目类别
        govItem['purchase_method'] = sel.xpath('/html/body/div[2]/div[2]/table/tr[2]/td[1]/text()').extract_first()
        # 采购方式
        govItem['proj_name'] = sel.xpath('/html/body/div[2]/div[2]/table/tr[2]/td[2]/text()').extract_first()
        # 项目名称
        govItem['purchase_company'] = sel.xpath('/html/body/div[2]/div[2]/table/tr[3]/td[1]/text()').extract_first()
        # 采购单位
        govItem['agent_agencies'] = sel.xpath('/html/body/div[2]/div[2]/table/tr[3]/td[2]/text()').extract_first()
        # 代理机构
        govItem['proj_budget'] = sel.xpath('/html/body/div[2]/div[2]/table/tr[4]/td[1]/text()').extract_first()
        # 项目预算
        govItem['public_time'] = sel.xpath('/html/body/div[2]/div[2]/table/tr[4]/td[2]/text()').extract_first()
        # 公示时间

        # 下面为正文部分的抽取
        titleStr = sel.xpath('//*[@id="tab1"]/div[1]/text()').extract_first()

        govItem['public_title'] = titleStr

        govItem['proj_city'] = "苏州"

        temp_url = self.processURL(sel.xpath('//*[@id="tab4"]//a/@href').extract_first())
        govItem['fileURL'] = "http://www.zfcg.suzhou.gov.cn/" + temp_url
        
        yield govItem
        # # sava htmls
        # global count
        # filename = './gov_html/gov-proj' + str(count) + '.html' 
        # count += 1
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
    def isExist(self, string):
        if "无" in string:
            return False
        else:
            return True
    def processURL(self, url):
        count = 0
        for i in url:
            if(i.isalnum()==False):
                count+=1
            else:
                break
        url = url[count:]
        return url