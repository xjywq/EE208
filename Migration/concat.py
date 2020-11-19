#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@Description : concat two database(Goods.dangdang_sport_item_detail, Goods.dangdang_sport_item)
@Date        : 2020/11/19 22:15:46
@Author      : xjywq
'''


import pymysql
import logging

logging_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='concat.log', level=logging.DEBUG, format=logging_FORMAT)

conn = pymysql.connect(host='121.199.77.180', port=3306, user='root',
                       passwd='Zrh999999', db='Goods', charset="utf8mb4")
cursor = conn.cursor()

cursor.execute("SELECT * FROM Goods.dangdang_sport_item_detail")
item_detail = cursor.fetchall()

for detail in item_detail:
    item = []
    # id, title, url, pic_url, price, hotword, score, comments, comments_tag, category, brand_id, brand
    cursor.execute("SELECT * FROM Goods.dangdang_sport_item WHERE `url`=%s",(detail[0]))
    i = cursor.fetchone()
    try:
        item.append(detail[0][-15:-5]) # id
        item.append(i[1]) # title
        item.append(detail[0]) # url
        item.append(detail[1]) # pic_url
        item.append(i[3][1:]) # price
        item.append(i[4]) # hotword
        item.append(detail[3]) # score
        item.append(detail[4]) # comments
        item.append(detail[5]) # comments_tag
        item.append(detail[2]) # category
        item.append(i[0]) # brand_id
        item.append(i[5]) # brand
        cursor.execute("REPLACE INTO DD_PE_item (id, Name, url, image_url, price, hotword, score, comment, comment_tag, category, brand_id, brand) \
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (item))
        conn.commit()
    except Exception as Err:
        logging.log(Err, "item "+detail[0][-15:-5]+" not found")