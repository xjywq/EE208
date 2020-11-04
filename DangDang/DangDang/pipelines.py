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
                cursor.execute("INSERT IGNORE INTO dangdang_sport (Id, Name, url) \
                                VALUES (%s, %s, %s)", (item["Id"], item["name"], item["url"]))
                conn.commit()
            except Exception as Err:
                logger.warning(Err, item)

        elif item["dealwith"] == "Item":
            try:
                # Insert
                # print(item)
                
                cursor.execute("REPLACE INTO dangdang_sport_item (id, title, url, price, hot_word, brand)\
                    VALUES (%s, %s, %s, %s, %s, %s)", (item['brand'], item['title'], item['url'], item['price'], item['hot_word'], item['from']))
                conn.commit()
                pass
            except Exception as Err:
                logger.warning(Err, item)

        elif item["dealwith"] == "Detail":
            # Todo 将item存入数据库
            try:
                # update
                cursor.execute("REPlACE INTO dangdang_sport_item_detail (page_url, img_urls, category, score, comments, comment_tag)\
                    VALUES (%s, %s, %s, %s, %s, %s)", (item['page_url'], str(item['img_urls']), item['category'], item['score'], item['comments'], item['comment_tag']))

                pass
            except Exception as Err:
                logger.warning(Err, item)
            pass

        return item
