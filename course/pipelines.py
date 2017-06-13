# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
from scrapy.conf import settings
import pymongo
import re
import csv
import os


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class GeekCollegePipeline(object):
    def __init__(self):
        self.host = settings['MONGODB_HOST']
        self.port = settings['MONGODB_PORT']
        self.db_name = settings['MONGODB_DBNAME']
        self.doc_name = settings['MONGODB_DOCNAME']

    def open_spider(self, spider):
        '''在spider开始后执行,一般用来连接数据库等操作。
        INFO: Spider opened ---> 调用本函数'''
        client = pymongo.MongoClient(host=self.host, port=self.port)
        tdb = client[self.db_name]
        self.post = tdb[self.doc_name]
        pass

    def process_item(self, item, spider):
        '''在捕捉到item的时候执行，一般我们会在这里做数据过滤并且把数据存入数据库。'''
        if not self.db_exist(item):
            title = item['title'][0]
            desc = re.sub('[\n\t]*', '', item['desc'][0])
            link = re.sub('//', 'http://', item['link'][0])
            # course_info = [item['course_name'], title, desc, link]
            # self.save_to_csv(course_info)
            self.post.insert({'course_name': item['course_name'], 'title': title, 'description': desc, 'link': link})
            return item
        else:
            DropItem(item)

    def close_spider(self, spider):
        '''在spider结束的时候执行,一般用来断开数据库连接或者做数据收尾工作。
         INFO: Closing spider (finished) ---> 调用本函数'''
        pass

    def save_to_csv(self, course_info):
        self.creat_dir()
        with open('./data/Geek_college_course.csv', 'a+') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(course_info)

    def creat_dir(self):
        if not os.path.isdir('./data'):
            os.mkdir('./data')

    def db_exist(self, item):
        '''判断课程在数据库中是否存在，存在则为true，不存在为false'''
        flag = False
        for each in self.post.find({'title': item['title'][0]}):
            flag = True
        return flag
