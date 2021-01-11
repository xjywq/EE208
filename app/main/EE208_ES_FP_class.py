import json
from elasticsearch import Elasticsearch
from collections import Counter
import jieba
import jieba.analyse
## import EE208_ES_FP_search

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
        keywords_list = jieba.analyse.extract_tags(i,topK = 10,withWeight = True, allowPOS = ())
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

class ES_FP_search():
    def __init__(self):
        self.es = Elasticsearch()

    def ES_keywords(self, domain, keywords):
        query = {
            "query": {
                "match": {
                    "{}".format(domain): "{}".format(keywords)
                }
            },
            "highlight":{
                "pre_tags":["<font>"],    # set the tag
                "post_tags":["</font>"],   # for example, you would get sth like this: xxx<font>highlight</font>
                "fields":{
                    "{}".format(domain):{}
                }
            },
            "from": 0,
            "size": 500
        }
        hit = self.es.search(index="dd_pe_item", body=json.dumps(query))
        result = []
        for entry in hit['hits']['hits']:
            dic = entry['_source']
            dic['image_url'] = entry['_source']['image_url'].split('#')
            dic['category'] = entry['_source']['category'].replace(u'\xa0', u' ').split('#')
            if domain in ['image_url','category']:
                dic['{}'.format(domain)] = entry['highlight']['{}'.format(domain)][0].replace(u'\xa0', u' ').split('#')
            else:
                dic['{}'.format(domain)] = entry['highlight']['{}'.format(domain)][0]
            result.append(dic)
        return result

    def ES_combinesearch(self, domain1, keywords1, domain2, keywords2): # domain1: 主要搜索词 domain2： 限制词
        query = {
            "query":{
                "bool":{
                    "must":[
                        {
                            "match":{
                                "{}".format(domain1): "{}".format(keywords1)
                            }
                        }
                    ],
                    "filter":{
                        "match":{
                            "{}".format(domain2): "{}".format(keywords2)
                        }
                    }
                }
            },
            "highlight":{
                "pre_tags":["<font>"],    # set the tag
                "post_tags":["</font>"],   # for example, you would get sth like this: xxx<font>highlight</font>
                "fields":{
                    "{}".format(domain1):{}
                }
            },
            "from": 0,
            "size": 500
        }
        hit = self.es.search(index="dd_pe_item", body=json.dumps(query))
        result = []
        for entry in hit['hits']['hits']:
            dic = entry['_source']
            dic['image_url'] = entry['_source']['image_url'].split('#')
            dic['category'] = entry['_source']['category'].replace(u'\xa0', u' ').split('#')
            if domain in ['image_url','category']:
                dic['{}'.format(domain)] = entry['highlight']['{}'.format(domain)][0].replace(u'\xa0', u' ').split('#')
            else:
                dic['{}'.format(domain)] = entry['highlight']['{}'.format(domain)][0]
            result.append(dic)
        return result

    def ES_scopesearch(self, domain1, keywords, domain2, gte, lte):
        query = {
            "query":{
                "bool":{
                    "must":[
                        {
                            "match":{
                                "{}".format(domain1): "{}".format(keywords)
                            }
                        }
                    ],
                    "filter":{
                        "range":{
                            "{}".format(domain2):{
                                "gte": "{}".format(gte),
                                "lte": "{}".format(lte),
                            }
                        }
                    }
                }
            },
            "highlight":{
                "pre_tags":["<font>"],    # set the tag
                "post_tags":["</font>"],   # for example, you would get sth like this: xxx<font>highlight</font>
                "fields":{
                    "{}".format(domain1):{}
                }
            },
            "from": 0,
            "size": 500
        }
        hit = self.es.search(index="dd_pe_item", body=json.dumps(query))
        result = []
        for entry in hit['hits']['hits']:
            dic = entry['_source']
            dic['image_url'] = entry['_source']['image_url'].split('#')
            dic['category'] = entry['_source']['category'].replace(u'\xa0', u' ').split('#')
            if domain1 in ['image_url','category']:
                dic['{}'.format(domain1)] = entry['highlight']['{}'.format(domain1)][0].replace(u'\xa0', u' ').split('#')
            else:
                dic['{}'.format(domain1)] = entry['highlight']['{}'.format(domain1)][0]
            result.append(dic)
        return result


'''
result = [
    {
        'id' = 'str'
        'title' = 'str'
        'url' = 'str'
        'image_url' = [list]
        'category' = [list]
        'brand' = 'str'
        'brand_id' = int
        'score' = double
        'price' = int
        'hotword' = 'str'
        'rate' = float
    }
]
'''




if __name__ == '__main__':
    search = ES_FP_search()
    domain = 'title'#input("")
    keywords = '卫衣'#input("")
    domain2 = 'price'#input("")
    keywords2 = '297'# input("")
    gte = '200' # input("")
    lte = '100' # input("")
    result = search.ES_keywords(domain, keywords)
    print(result)
    result = search.ES_combinesearch(domain, keywords, domain2, keywords2)
    print(result)
    result = search.ES_scopesearch(domain, keywords, domain2, gte, lte)