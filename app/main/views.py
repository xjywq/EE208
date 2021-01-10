import json

from flask import Flask, redirect, render_template, request, session, url_for

from .. import db
from ..models import SportItem
from . import main
from .EE208_ES_FP_class import ES_FP_search
from .forms import SearchForm
from .WordCloud import cut_comment_seg, wordcloud_base

from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        form = SearchForm()
        return render_template("index.html", form=form)
    else:
        
        form = SearchForm(formdata=request.form)
        if form.validate():  # 对用户提交数据进行校验，form.data是校验完成后的数据字典
            print("用户提交的数据用过格式验证，值为：%s" % form.data)
            return "登录成功"
        else:
            print(form.errors, "错误信息")
        return render_template("index.html", form=form)


@main.route('/result', methods=['POST'])
def result():
    form = SearchForm(formdata=request.form)
    if form.validate():  # 对用户提交数据进行校验，form.data是校验完成后的数据字典
        print("用户提交的数据用过格式验证，值为：{}".format(form.data))
        command = form.data["content"]
        # Todo search
        search_res = SportItem.query.filter_by(id=int(command)).first()
        # 我们认为search_res是一个数组，首先统计一下，然后下载pagination
        found = len(search_res)
        page = request.args.get(get_page_parameter(), type=int, default=1)
        
        per_page = int(request.args.get('per_page', default = 40)) # 这样可以整除
        # 要传进template的代码
        res = [single for single in search_res[(page - 1) * per_page, page * per_page]]
        res = [[each for each in res[i * 4, i * 4 + 4]] for i in range(per_page / 4)]
        
        pagination = Pagination(found = found, page = page, search = True, total = found, per_page = per_page)
        return render_template('result.html', res=res, keyword = form.data, pagenation = pagination)
    else:
        print(form.errors, "错误信息")
    return render_template("index.html", form=form)


@main.route('/item', methods=["GET"])
def item():
    item_id = request.args.get('id')
    item_item = SportItem.query.filter_by(id=int(item_id)).first()
    item_detail = {}
    item_detail["image_url"] = json.loads(item_item.image_url)
    item_detail["image_url"] = list(enumerate(item_detail["image_url"]))

    # Comment Data
    comment_num = json.loads(item_item.comment_num)
    item_detail['rate'] = comment_num[-1]
    item_detail['buy_num'] = int(comment_num[0])
    item_detail['comment_num'] = int(comment_num[1])
    item_detail['default_num'] = int(comment_num[2]) - int(comment_num[1])
    item_detail['good_num'] = int(
        comment_num[1]) - int(comment_num[3]) - int(comment_num[4])
    item_detail['middle_num'] = int(comment_num[3])
    item_detail['bad_num'] = int(comment_num[4])
    comment = json.loads(item_item.comment)[:5]
    item_detail['comment'] = []
    for com in comment:
        s1 = com[0].replace('u', '\\u')
        s1 = eval('u"%s"' % s1)
        s2 = com[1].replace('u', '\\u')
        s2 = eval('u"%s"' % s2)
        item_detail['comment'].append([s1, s2, com[2]])

    # Recommand
    es_fp = ES_FP_search()
    brand_res = es_fp.ES_keywords("brand", item_item.brand)[:6]
    brand_res = brand_res + [{'id': 0, 'title': '商品示例', 'url': '/', 'image_url': ['http://img3m9.ddimg.cn/74/17/1338216239-1_u_8.jpg'],
                              'keywords': [], 'brand': '暂无', 'brand_id': 0, 'score': 0, 'price': 0, 'hotword': ''}] * (6-len(brand_res))
    es_fp = ES_FP_search()
    search_res = es_fp.ES_keywords("title", item_item.Name)[1:7]
    search_res = search_res + [{'id': 0, 'title': '商品示例', 'url': '/', 'image_url': ['http://img3m9.ddimg.cn/74/17/1338216239-1_u_8.jpg'],
                                'keywords': [], 'brand': '暂无', 'brand_id': 0, 'score': 0, 'price': 0, 'hotword': ''}] * (6-len(search_res))
    recommand = [search_res, brand_res]

    # WordCloud
    c = wordcloud_base()
    c.dump_options_with_quotes()

    return render_template("item.html", item_detail=item_detail, recommand=recommand, item=item_item)


@main.route("/wordcloudChart")
def get_wordcloud_chart():
    c = wordcloud_base()
    return c.dump_options_with_quotes()
        
