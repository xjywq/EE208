# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import logging
import pymysql
# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

logger = logging.getLogger(__name__)

conn = pymysql.connect(host='121.199.77.180', port=3306, user='root',
                       passwd='Zrh999999', db='Goods', charset="utf8mb4")
cursor = conn.cursor()

Category = {} # 暂存品牌


class ProcessPipeline:
    def process_item(self, item, spider):
        if item["dealwith"] == "Category":
            Category[item["name"]] = item["Id"]

        elif item["dealwith"] == "Item":
            item["brand"] = Category[item["from"]]
            # brand is an id number 
        elif item["dealwith"] == "Detail":
            # Todo 后续数据处理, 不过好像没用上
            pass

        return item


class SavePipeline:

    def process_item(self, item, spider):
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
                cursor.execute("REPLACE INTO DD_PE_item (id, Name, url, price, hotword, brand)\
                    VALUES (%s, %s, %s, %s, %s, %s)", (item['brand'], item['title'], item['url'], item['price'], item['hot_word'], item['from']))
                conn.commit()
                # print("upload item of :  " , item["title"])
            except Exception as Err:
                logger.error(Err)
                logger.error(item)

        elif item["dealwith"] == "Detail":
            try:
                cursor.execute("UPDATE DD_PE_item SET (image_url, category, score, comment, comment_tag) = \
                    (%s, %s, %s, %s, %s, %s) WHERE url = %s" , (str(item['img_urls']), item['category'], item['score'], item['comments'], item['comment_tag'], item['page_url']))
                conn.commit()
                # print("upload detail of :  " , item["category"])
            except Exception as Err:
                logger.error(Err)
                logger.error(item)

        return item
