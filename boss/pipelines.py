# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql
from twisted.enterprise import adbapi
from datetime import datetime
import pymongo

class BossPipeline(object):
    def __init__(self):
        self.file = open("work.json","wb")

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False)+"\n"
        self.file.write(content.encode("utf-8"))
        return item

    def close_spider(self, spider):
        self.file.close()

class BossTwistedMysqlPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.do_insert, item)

    @classmethod
    def from_crawler(cls, crawler):
        params = dict(
            host = crawler.settings['MYSQL_HOST'],
            user = crawler.settings['MYSQL_USER'],
            password = crawler.settings['MYSQL_PASSWORD'],
            database = crawler.settings['MYSQL_DB'],
            charset = "utf8",
            use_unicode = True,
        )
        dbpool = adbapi.ConnectionPool("pymysql", **params)
        return cls(dbpool)

    def do_insert(self, cursor, item):
        into_sql ='''
            insert into zhipin(position_name,salary,city,work_experience,education,tags,describes,\
            company_describe,information,work_location,company_name,company_url,url,url_object_id, crawl_time)\
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE salary = VALUES(salary)
        '''
        crawl_time = datetime.now()
        params = (item['position_name'],item['salary'],item['city'],item['work_experience'],item['education'],\
                  item['tags'],item['describes'],item['company_describe'],item['information'],\
                  item['work_location'],item['company_name'],item['company_url'],item['url'],\
                  item['url_object_id'], crawl_time)
        cursor.execute(into_sql, params)


class BossMongodbPipeline(object):
    def __init__(self, table):
        self.table = table

    @classmethod
    def from_crawler(cls, crawler):
        client = pymongo.MongoClient(host=crawler.settings['MONGO_HOST'])
        db = client[crawler.settings['MONGO_DB']]
        table = db[crawler.settings['MONGO_TABLE']]
        return cls(table)

    def process_item(self, item, spider):
        data = dict(item)
        self.table.insert(data)
        return item



