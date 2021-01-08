# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import json
import logging

import pymysql
from password import onlinepassword as pd
# from password import mypassword as pd

# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

logger = logging.getLogger(__name__)

conn = pymysql.connect(host=pd['host'], port=3306, user=pd['user'],
                       passwd=pd['passwd'], db='Goods', charset="utf8mb4")


Category = {}  # 暂存品牌


class ProcessPipeline:
    def process_item(self, item, spider):
        # if item["dealwith"] == "Category":
        #     Category[item["name"]] = item["Id"]

        # elif item["dealwith"] == "Item":
        #     item["brand"] = Category[item["from"]]
        #     # brand is an id number
        pass
        return item


class SavePipeline:

    def process_item(self, item, spider):
        cursor = conn.cursor()
        if item["dealwith"] == "Category":
            try:
                cursor.execute("REPLACE INTO dangdang_sport (Id, Name, url) \
                                VALUES (%s, %s, %s)", (item["Id"], item["name"], item["url"]))
                conn.commit()
                # print("upload category of :  " , item["name"])
            except Exception as Err:
                logger.error(Err)
                logger.error(item)

        elif item["dealwith"] == "Item":
            try:
                cursor.execute('REPLACE INTO DD_PE_item (id, Name, url, price, hotword, brand, brand_id)\
                    VALUES (%s, %s, %s, %s, %s, %s, %s)', (item['id'], item['title'], item['url'], item['price'], item['hot_word'], item['from'], item['brand']))
                conn.commit()
                # print("upload item of :  " , item["title"])
            except Exception as Err:
                logger.error(Err)
                logger.error(item)

        elif item["dealwith"] == "Detail":
            try:
                cursor.execute("UPDATE `DD_PE_item` SET `image_url` = \
                    \'{}\' WHERE `id` = {}".format(json.dumps(item['img_urls']), item['id']))
                cursor.execute("UPDATE `DD_PE_item` SET `score` = \
                    \'{}\' WHERE `id` = {}".format(item['score'], item['id']))
                cursor.execute("UPDATE `DD_PE_item` SET `category` = \
                    \'{}\' WHERE `id` = {}".format(item['category'], item['id']))
                conn.commit()
                # print("upload detail of :  " , item["category"])
            except Exception as Err:
                logger.error(Err)
                logger.error(item)

        elif item["dealwith"] == "comment":
            try:
                cursor.execute("UPDATE `DD_PE_item` SET `comment` = \
                    \'{}\' WHERE `id` = {}".format(json.dumps(item['comment']), item['id']))
                conn.commit()

            except Exception as Err:
                logger.error(Err)
                logger.error(item)

        elif item["dealwith"] == "comment_tag":
            try:
                cursor.execute("UPDATE `DD_PE_item` SET `comment_tag` = \
                    \'{}\' WHERE `id` = {}".format(json.dumps(item['comment_tag']), item['id']))
                conn.commit()

            except Exception as Err:
                logger.error(Err)
                logger.error(item)

        return item
