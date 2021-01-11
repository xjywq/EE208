import json
from collections import Counter

import jieba
import jieba.analyse
from elasticsearch import Elasticsearch
from pymysql import connect
from snownlp import SnowNLP

from password import onlinepassword as pd


def cut_comment_seg(comment_all):
    c = Counter()
    if comment_all == None or comment_all == '[]':
        return str(c.most_common())
    f = []
    try:
        for i in eval(comment_all):
            comment = '\\u'.join(i[0].split('u'))
            comment = eval('u"%s"' % comment)
            f.append(comment)
    except:
        return str(c.most_common())
    keywords = []
    for i in f:
        keywords_list = jieba.analyse.extract_tags(
            i, topK=10, withWeight=True, allowPOS=())
        for j in keywords_list:
            keywords.append(j[0])
        # modify topK to change t.n.f result
    for x in keywords:
        if len(x) > 1 and x != '\r\n':
            c[x] += 1
    return str(c.most_common())


def recommend_item(comment_all):
    if comment_all == None or comment_all == '[]':
        sentiment = 0
    else:
        sentiment = 0
        try:
            for i in eval(comment_all):
                comment = '\\u'.join(i[0].split('u'))
                comment = eval('u"%s"' % comment)
                s = SnowNLP(comment)
                sentiment = sentiment + s.sentiments
            sentiment /= len(eval(comment_all))
        except:
            sentiment = 0
    return sentiment


es = Elasticsearch()
mappings = {
    "mappings": {
        "properties": {
            "paper_id": {
                "type": "long",
                "index": True
            },
            "title": {
                "type": "text",
                "index": True,
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_max_word"
            },
            "url": {
                "type": "text",
                "index": False
            },
            "img_url": {
                "type": "text",
                "index": False
            },
            "category": {
                "type": "text",
                "index": True,
                "analyzer": "ik_smart",
                "search_analyzer": "ik_smart"
            },
            "brand": {
                "type": "text",
                "index": True,
                "analyzer": "ik_smart",
                "search_analyzer": "ik_smart"
            },
            "brand_id": {
                "type": "long",
                "index": True
            },
            "score": {
                "type": "float",
                "index": False
            },
            "price": {
                "type": "float",
                "index": True
            },
            "hotword": {
                "type": "text",
                "index": False
            },
            "rate": {
                "type": "float",
                "index": False
            },
            "keywords": {
                "type": "text",
                "index": False
            }
        }
    }
}

if not es.indices.exists('dd_pe_item'):
    es.indices.create(index='dd_pe_item', body=mappings)
else:
    es.indices.delete('dd_pe_item')
    es.indices.create(index='dd_pe_item', body=mappings)

print("getting data")

database = connect(host=pd['host'], port=3306, user=pd['user'],
                   passwd=pd['passwd'], db='Goods', charset="utf8mb4")
cursor = database.cursor()
cursor.execute("SELECT * from DD_PE_item_test")
result = cursor.fetchall()


for item in result:
    comment_all = item[9]
    recommend_score = recommend_item(comment_all)
    cursor.execute("UPDATE DD_PE_item_test SET `score` = %s WHERE `id` = %s",
                   (recommend_score*100, item[0]))
    database.commit()
    comment_keywords = cut_comment_seg(comment_all)
    if item[11] == None:
        hotword = 'None'
    else:
        hotword = item[11]
    info = {
        'id': int(item[0]),
        'title': item[1],
        'url': item[2],
        'image_url': "#".join(eval(item[3])),
        'category': "#".join(item[4].split('>')),
        'brand': item[5],
        'brand_id': item[6],
        'score': recommend_score*100,
        'price': int(item[8]),
        'hotword': hotword,
        'rate': eval(item[12])[5],
        'keywords': comment_keywords
    }

    es.index(index='dd_pe_item', id=info['id'],
             body=json.dumps(info, ensure_ascii=False))

#     (1000245077, ' Adidas阿迪达斯 NEO 女子 运动外套 防风休闲棒球服CD2103',
#     'http://product.dangdang.com/1000245077.html', "['http://img3m7.ddimg.cn/62/27/1000245077-1_x_1.jpg', 'http://img3m7.ddimg.cn/62/27/1000245077-2_x_1.jpg', 'http://img3m7.ddimg.cn/62/27/1000245077-3_x_1.jpg', 'http://img3m7.ddimg.cn/62/27/1000245077-4_x_1.jpg', 'http://img3m7.ddimg.cn/62/27/1000245077-5_x_1.jpg', 'http://img3m7.ddimg.cn/62/27/1000245077-6_x_1.jpg']",
#      '运动户外>运动服装>夹克/外套>adidas夹克/外套>Adidas阿迪达斯\xa0NEO\xa0女子\xa0运动外套\xa0
# 防风休闲棒球服CD2103', 'adidas', 18493, 0.0, 616.0, 'NULL', 'NULL', None)
