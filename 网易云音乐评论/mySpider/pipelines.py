# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MyspiderPipeline(object):
    def process_item(self, item, spider):
        return item

import csv
class LiepingPieline(object):
    def __init__(self):
        self.headname = [
            'postTitle', 'postSalary', 'need_year', 'postExperience','company','company_url','infos'
        ]
        self.search = input('保存文件名：')
        self.f = open('E:\python_code\Search\datas\猎聘\招聘('+self.search+').csv','a',encoding='utf-8', newline='')
        self.writer = csv.DictWriter(self.f, self.headname)    #生成写对象
        self.writerheader = self.writer.writeheader() #写入表头

    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item

    def close_spider(self,spider):
        self.f.close()

