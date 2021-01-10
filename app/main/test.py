from .EE208_ES_FP_class import ES_FP_search

if __name__ == "__main__":
    es_fp = ES_FP_search()
    print(es_fp.ES_scopesearch('title', '耐克', 'price', "100", "200"))