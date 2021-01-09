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
            }
        }
        hit = self.es.search(index="dd_pe_item", body=json.dumps(query))
        result = []
        for entry in hit['hits']['hits']:
            dic = entry['_source']
            dic['score'] = entry['_score']
            dic['image_url'] = entry['_source']['image_url'].split('#')
            dic['keywords'] = entry['_source']['keywords'].replace(u'\xa0', u' ').split('#')
            result.append(dic)
        return result

    def ES_combinesearch(self, domain1, keywords1, domain2, keywords2):
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
            }
        }
        hit = self.es.search(index="dd_pe_item", body=json.dumps(query))
        result = []
        for entry in hit['hits']['hits']:
            dic = entry['_source']
            dic['score'] = entry['_score']
            dic['image_url'] = entry['_source']['image_url'].split('#')
            dic['keywords'] = entry['_source']['keywords'].replace(u'\xa0', u' ').split('#')
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
            }
        }
        hit = self.es.search(index="dd_pe_item", body=json.dumps(query))
        result = []
        for entry in hit['hits']['hits']:
            dic = entry['_source']
            dic['score'] = entry['_score']
            dic['image_url'] = entry['_source']['image_url'].split('#')
            dic['keywords'] = entry['_source']['keywords'].replace(u'\xa0', u' ').split('#')
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
    domain2 = 'price'#input("")
    keywords2 = '200'# input("")
    gte = '200' # input("")
    lte = '100' # input("")
    result = search.ES_keywords(domain, keywords)
    print(result)
    result = search.ES_combinesearch(domain, keywords, domain2, keywords2)
    print(result)
    result = search.ES_scopesearch(domain, keywords, domain2, gte, lte)