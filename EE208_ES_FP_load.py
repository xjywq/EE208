from pymysql import connect
from elasticsearch import Elasticsearch
from password import onlinepassword as pd
import json

database = connect(host=pd['host'], port=3306, user=pd['user'],
                       passwd=pd['passwd'], db='Goods', charset="utf8mb4")

cursor = database.cursor()
cursor.execute("SELECT * from DD_PE_item_test WHERE `image_url` is not NULL")
result = cursor.fetchall()

print("creating")
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
                "index": True
            },
            "price": {
                "type": "float",
                "index": True
            },
            "hotword": {
                "type": "text",
                "index": True
            }
        }
    }
}


if es.indices.exists("dd_pe_item"):
    print('索引存在')
else:
    print('索引不存在')
    es.indices.create(index='dd_pe_item', body=mappings)
print("indexing")
num = 1
for item in result:
    if item[11] == None:
        hotword = 'None'
    else:
        hotword = item[11]
    info = {
        'id': int(item[0]),
        'title': item[1],
        'url': item[2],
        'image_url': "#".join(json.loads(item[3])),
        'keywords': "#".join(item[4].split('>')),
        'brand': item[5],
        'brand_id': item[6],
        'score': int(item[7]),
        'price': int(item[8]),
        'hotword': hotword
    }

    num += 1

    es.index(index='dd_pe_item', id=info['id'],
             body=json.dumps(info, ensure_ascii=False))

#     (1000245077, ' Adidas阿迪达斯 NEO 女子 运动外套 防风休闲棒球服CD2103',
#     'http://product.dangdang.com/1000245077.html', "['http://img3m7.ddimg.cn/62/27/1000245077-1_x_1.jpg', 'http://img3m7.ddimg.cn/62/27/1000245077-2_x_1.jpg', 'http://img3m7.ddimg.cn/62/27/1000245077-3_x_1.jpg', 'http://img3m7.ddimg.cn/62/27/1000245077-4_x_1.jpg', 'http://img3m7.ddimg.cn/62/27/1000245077-5_x_1.jpg', 'http://img3m7.ddimg.cn/62/27/1000245077-6_x_1.jpg']",
#      '运动户外>运动服装>夹克/外套>adidas夹克/外套>Adidas阿迪达斯\xa0NEO\xa0女子\xa0运动外套\xa0
# 防风休闲棒球服CD2103', 'adidas', 18493, 0.0, 616.0, 'NULL', 'NULL', None)
