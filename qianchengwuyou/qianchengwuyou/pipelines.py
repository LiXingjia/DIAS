# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector
import json
import os
from scrapy.exceptions import DropItem



class QianchengwuyouPipeline(object):
    def process_item(self, item, spider):
        return item


# 筛选信息
class CompareInfo(object):
    def open_spider(self, spider):
        # 不同spider选择不同文件
        self.oldfile = 'record/'+spider.name + '_old.json'
        self.newfile = 'record/'+spider.name + '_new.json'
        # 打开文件
        # 若存在，打开文件，读取数据后删除
        if os.path.exists(self.oldfile):
            old = open(self.oldfile, 'r')
            self.olddata = json.load(old)
            # 关闭旧文件
            old.close()
            # 删除旧文件
            os.remove(self.oldfile)
        # 不存在，就赋值空list
        else:
            self.olddata = []
        # 新建新文件,保存新一轮数据
        self.new = open(self.newfile, 'w')
        self.newdata = []

    def process_item(self, item, spider):
        # 种子为jobName和Company
        data = {'jobName': item['jobName'], 'company': item['company']}
        # 过程：
        # 1、把所有item写入新文件。对每一条item比对一下旧文件中是否存在，如果是，从旧记录中删除此条信息，之后丢弃此item，因为在之前已经写入数据库了，不用再写入了
        # 2、对旧文件中剩余的信息从数据库删除掉；
        # 3、把新文件改名为旧文件，关闭新文件。
        self.newdata.append(data)
        if data in self.olddata:
            # 若已有则删除
            self.olddata.remove(data)
            # 丢弃此item
            raise DropItem(item)
        # 对旧文件中剩余的信息从相应数据表中删除掉，因为这部分信息在原网站不存在了
        if self.olddata:
            conn = mysql.connector.connect(user='DIAS', password='84877178', database='dias')
            cursor = conn.cursor()
            for each in self.olddata:
                delete_sql = "delete from "+spider.settings['BOT_NAME']+"_"+spider.name+"where jobName =" + each['jobName'] + "and company ="+each['company']
                cursor.execute(delete_sql)
                conn.commit()
            cursor.close()
            conn.close()
        return item

    def close_spider(self, spider):
        # 写入新文件
        self.new.write(json.dumps(self.newdata, ensure_ascii=False))
        # 关闭新文件
        self.new.close()
        # 新文件改名为旧文件
        os.rename(self.newfile, self.oldfile)


# 写入数据库
class WriteIntoDB(object):
    def __init__(self):
        self.conn = mysql.connector.connect(user='DIAS', password='84877178', database='dias')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # 根据spider名字选择不同的表
        insert_sql = "insert into "+spider.settings['BOT_NAME']+"_" + spider.name + "(jobName,jobType, company, companyType, salary, city, workingExp, eduLevel, welfare, timestate, detail) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (item['jobName'], item['jobType'], item['company'], item['companyType'], item['salary'], item['city'], item['workingExp'], item['eduLevel'], item['welfare'], item['timestate'], item['detail'])
        self.cursor.execute(insert_sql, data)
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

