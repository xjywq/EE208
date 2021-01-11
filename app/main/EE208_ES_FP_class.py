import json
from elasticsearch import Elasticsearch


## import EE208_ES_FP_search


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
                "pre_tags":['<font style="color: red;">'],    # set the tag
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
            dic['score'] = entry['_score']
            dic['image_url'] = entry['_source']['image_url'].split('#')
            dic['keywords'] = entry['_source']['keywords'].replace(u'\xa0', u' ').split('#')
            if domain in ['image_url','keywords']:
                dic['{}'.format(domain)] = entry['highlight']['{}'.format(domain)][0].replace(u'\xa0', u' ').split('#')
            else:
                dic['{}'.format(domain)] = entry['highlight']['{}'.format(domain)][0]
            result.append(dic)
        return result

    def ES_combinesearch(self, domain1, keywords1, domain2=None, keywords2=None): # domain1: 主要搜索词 domain2： 限制词
        if keywords2 is None:
            return self.ES_keywords(domain1, keywords1)
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
                "pre_tags":['<font style="color: red;">'],    # set the tag
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
            dic['score'] = entry['_score']
            dic['image_url'] = entry['_source']['image_url'].split('#')
            dic['keywords'] = entry['_source']['keywords'].replace(u'\xa0', u' ').split('#')
            if domain1 in ['image_url','keywords']:
                dic['{}'.format(domain1)] = entry['highlight']['{}'.format(domain1)][0].replace(u'\xa0', u' ').split('#')
            else:
                dic['{}'.format(domain1)] = entry['highlight']['{}'.format(domain1)][0]
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
                "pre_tags":['<font style="color: red;">'],    # set the tag
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
            dic['score'] = entry['_score']
            dic['image_url'] = entry['_source']['image_url'].split('#')
            dic['keywords'] = entry['_source']['keywords'].replace(u'\xa0', u' ').split('#')
            if domain1 in ['image_url','keywords']:
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
        'keywords' = [list]
        'brand' = 'str'
        'brand_id' = int
        'score' = double
        'price' = int
        'hotword' = 'str'
    }
]
'''




if __name__ == '__main__':
    search = ES_FP_search()
    domain = 'brand'#input("")
    keywords = '安踏'#input("")
    result = search.ES_keywords(domain, keywords)
    print(len(result))
    # domain2 = 'price'#input("")
    # keywords2 = '200'# input("")
    # gte = '200' # input("")
    # lte = '100' # input("")
    # result = search.ES_keywords(domain, keywords)
    # print(result)
    # result = search.ES_combinesearch(domain, keywords, domain2, keywords2)
    # print(result)
    # result = search.ES_scopesearch(domain, keywords, domain2, gte, lte)
