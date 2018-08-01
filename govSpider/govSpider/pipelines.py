# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymysql
import pymysql.cursors
from scrapy.conf import settings

class GovspiderPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset=settings['CHARSET'],
            use_unicode=True)
        # 通过cursor执行增删查改
        logging.info("mysql connect succes!")#测试语句，这在程序执行时非常有效的理解程序是否执行到这一步
        self.cursor = self.connect.cursor();#通过cursor进行增删改查
    def process_item(self, item, spider):
        try:
            # 查重处理  用proj_name作为Key进行查询
            self.cursor.execute(
                """select * from suzhou where proj_name = %s""",
                item['proj_name'])
            # 是否有重复数据
            repetition = self.cursor.fetchone()
            # 重复
            if repetition:
                pass
            else:
                # 插入数据
                self.cursor.execute(
                    """insert into suzhou( label_tender, 
                                        label_notice, 
                                        label_winBid,
                                        label_purchaseFile,
                                        label_purchaseContract, 
                                        label_dealContract,
                                        proj_area,
                                        proj_class,
                                        purchase_method,
                                        proj_name,
                                        purchase_company,
                                        agent_agencies,
                                        proj_budget,
                                        public_time,
                                        public_title,
                                        proj_city,
                                        fileURL
                                        )
                    value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (item['label_tender'],
                    item['label_notice'],
                    item['label_winBid'],
                    item['label_purchaseFile'],
                    item['label_purchaseContract'],
                    item['label_dealContract'],
                    item['proj_area'],
                    item['proj_class'],
                    item['purchase_method'],
                    item['proj_name'],
                    item['purchase_company'],
                    item['agent_agencies'],
                    item['proj_budget'],
                    item['public_time'],
                    item['public_title'],
                    item['proj_city'],
                    item['fileURL']))
                try:
                    self.connect.commit() # 提交sql语句
                    logging.info('sql commit success!')
                except Exception as error:
                    logging.warning(error)
        except Exception as error:
            # 出现错误时打印错误日志
            logging.warning(error)
        return item

