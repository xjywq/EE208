from flask import render_template, session, redirect, url_for, request, Flask
import json

from . import main
from .forms import SearchForm

from .. import db
from ..models import SportItem
from .EE208_ES_FP_class import ES_FP_search

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
        return render_template('result.html', res=search_res)
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
    # Todo change data
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
    # Todo search
    es_fp = ES_FP_search()
    brand_res = es_fp.ES_keywords("brand", item_item.brand)[:6]
    brand_res = brand_res + [{'id': 0, 'title': '商品示例', 'url': '/', 'image_url': ['http://img3m9.ddimg.cn/74/17/1338216239-1_u_8.jpg'], 'keywords': [], 'brand': '暂无', 'brand_id': 0, 'score': 0, 'price': 0, 'hotword': ''}] * (6-len(brand_res))
    es_fp = ES_FP_search()
    search_res = es_fp.ES_keywords("title", item_item.Name)[1:7]
    search_res = search_res + [{'id': 0, 'title': '商品示例', 'url': '/', 'image_url': ['http://img3m9.ddimg.cn/74/17/1338216239-1_u_8.jpg'], 'keywords': [], 'brand': '暂无', 'brand_id': 0, 'score': 0, 'price': 0, 'hotword': ''}] * (6-len(search_res))
    recommand = [search_res, brand_res]
    return render_template("item.html", item_detail=item_detail, recommand=recommand, item=item_item)


