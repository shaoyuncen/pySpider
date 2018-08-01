# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GovspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 内容部分
    # proj_content = scrapy.Field() # 招标公告内容

    # 正文部分

    public_title = scrapy.Field() # 公告标题

    fileURL = scrapy.Field() # 附件文件下载url

    proj_city = scrapy.Field() # 城市
    # 顶部8个属性
    proj_area = scrapy.Field() # 项目地区

    proj_class = scrapy.Field() # 项目类别

    purchase_method = scrapy.Field() #采购方式

    proj_name = scrapy.Field() # 项目名称

    purchase_company = scrapy.Field() #采购单位

    agent_agencies = scrapy.Field() #代理机构
        
    proj_budget = scrapy.Field() # 项目预算

    public_time = scrapy.Field() # 公示时间

    # 侧边6个标签
    label_tender = scrapy.Field() # 招标公告

    label_notice = scrapy.Field() # 补充通知
    
    label_winBid = scrapy.Field() # 中标公告
    
    label_purchaseFile = scrapy.Field() # 采购文件
    
    label_purchaseContract = scrapy.Field() # 采购合同
    
    label_dealContract = scrapy.Field() # 成交公告
    

    

