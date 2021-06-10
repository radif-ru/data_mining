# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .settings import BOT_NAME
from pymongo import MongoClient


class GbParsePipeline:

    def process_item(self, item, spider):
        return item


class GbMongoPipeline:

    def __init__(self):
        client = MongoClient()
        self.db = client[BOT_NAME]

    def process_item(self, item, spider):
        collection_name = f"{spider.name}_{item.get('item_type', '')}"
        self.db[collection_name].insert_one(item)
        return item
