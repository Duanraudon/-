# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#调用pymongo库
from pymongo import MongoClient
#编写MongoDBPipeline
class MongoDBPipeline(object):

    #定义一个从setting读取数据库地址，名称,集合名称的函数
    @classmethod
    def from_crawler(cls,crawler):
        cls.url = crawler.settings.get('MONGODB_DB_URL', 'mongodb://localhost:27017/')
        cls.dbname = crawler.settings.get('MONGODB_DB_NAME', 'default')
        cls.collectionname = crawler.settings.get('MONGODB_COLLECTION_NAME','default')
        return cls()

    #定义插入数据库的函数
    def process_item(self,item,spider):
        #连接数据库
        client = MongoClient(self.url)
        db = client[self.dbname]
        post = db[self.collectionname]
        #将item类型转化为字典类型
        dicts = dict(item)
        post.insert(dicts)
        return item

    #定义数据库连接关闭函数
    def close_spider(self,spider):
        self.client.close()

