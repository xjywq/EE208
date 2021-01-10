import json
import os
import re
import uuid

from config import basedir
from flask import (redirect, render_template, request, send_from_directory,
                   session, url_for)
from flask_paginate import Pagination, get_page_parameter
from werkzeug.datastructures import ImmutableMultiDict

from .. import db
from ..models import SportItem
from . import main
from .EE208_ES_FP_class import ES_FP_search
from .forms import SearchForm, UploadForm
from .WordCloud import cut_comment_seg, wordcloud_base


def query():
    pass
def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename

es_fp = ES_FP_search()
file_path = os.path.join(basedir, 'app', 'static', 'uploaded_files')
if os.path.exists(file_path):
    os.mkdir(file_path)


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        form = SearchForm()
        return render_template("index.html", form=form)
    else:
        
        form = SearchForm(formdata=request.form)
        print(request.form)
        if form.validate():  # 对用户提交数据进行校验，form.data是校验完成后的数据字典
            print("用户提交的数据用过格式验证，值为：%s" % form.data)
            return "登录成功"
        else:
            print(form.errors, "错误信息")
        return render_template("index.html", form=form)


@main.route('/result', methods=['GET'])
def result():

    form: SearchForm = SearchForm(formdata=ImmutableMultiDict([('content', request.args.get('content'))]))

    if form.validate():  # 对用户提交数据进行校验，form.data是校验完成后的数据字典
        print("用户提交的数据用过格式验证，值为：{}".format(form.data))
        def parseCommand(command):
            
            # allowed_opt = ['title', 'author', 'language']
            allowed_opt = ['price', 'brand']
            command_dict = {}
            opt = 'title'
            for i in command.split(' '):
                flag1 = ':' in i
                flag2 = '：' in i
                if flag1 or flag2:
                    if flag1:
                        opt, value = i.split(':')[:2]
                    else:
                        opt, value = i.split('：')[:2]
                    opt = opt.lower()
                    if opt in allowed_opt and value != '':
                        command_dict[opt] = command_dict.get(opt, '') + value
                else:
                    command_dict[opt] = command_dict.get(opt, '') + i
            return command_dict
        commands = form.data["content"].split()
        
        commands = parseCommand(form.data['content'])

        all_domains = list(commands.keys())
        length = len(all_domains)
        domain = 'title'
        keyword = commands.get('title', '')
        if length == 1:
            
            search_res = es_fp.ES_keywords(domain, keyword)
        else:
            domain2 = all_domains[1] if all_domains[0] == 'title' else all_domains[0]
            keyword2 = commands[domain2].split('-')
            search_res = es_fp.ES_scopesearch(domain, keyword, domain2, keyword2[0], keyword2[1])
            
            
        # Todo search
        # 我们认为search_res是一个数组，首先统计一下，然后下载pagination
        found = len(search_res)
        # page = request.form()
        page = request.args.get(get_page_parameter(), type=int, default=1)
        
        per_page = int(request.args.get('per_page', default = 20)) # 这样可以整除
        # print(found, type(page), type(per_page))
        # 要传进template的代码
        res = [single for single in search_res[(page - 1) * per_page: page * per_page]]
        # res = [[each for each in res[i * 2: i * 2 + 2]] for i in range(per_page // 2)]
        
        pagination = Pagination(found = found, page = page, search = True, total = found, per_page = per_page, bs_version = 4)
        return render_template('result.html', res=res, keyword = form.data['content'], pagination = pagination)
    else:
        print(form.errors, "错误信息")
    return render_template("index.html", form=form)


@main.route('/brand_result', methods=['GET'])
def brand_result():

    form: SearchForm = SearchForm(formdata=ImmutableMultiDict([('content', request.args.get('content'))]))
    print(form.data)
    if form.validate():  # 对用户提交数据进行校验，form.data是校验完成后的数据字典
        print("用户提交的数据用过格式验证，值为：{}".format(form.data))
        def parseCommand(command):
            # allowed_opt = ['title', 'author', 'language']
            allowed_opt = ['price', 'brand']
            command_dict = {}
            opt = 'brand'
            for i in command.split(' '):
                flag1 = ':' in i
                flag2 = '：' in i
                if flag1 or flag2:
                    if flag1:
                        opt, value = i.split(':')[:2]
                    else:
                        opt, value = i.split('：')[:2]
                    opt = opt.lower()
                    if opt in allowed_opt and value != '':
                        command_dict[opt] = command_dict.get(opt, '') + value
                else:
                    command_dict[opt] = command_dict.get(opt, '') + i
            return command_dict
        commands = form.data["content"].split()
        
        commands = parseCommand(form.data['content'])

        all_domains = list(commands.keys())
        length = len(all_domains)
        domain = 'brand'
        keyword = commands.get('brand', '')
        if length == 1:
            
            search_res = es_fp.ES_keywords(domain, keyword)
        else:
            domain2 = all_domains[1] if all_domains[0] == 'brand' else all_domains[0]
            keyword2 = commands[domain2].split('-')
            print(domain2, keyword2)
            search_res = es_fp.ES_scopesearch(domain, keyword, domain2, keyword2[0], keyword2[1])
        # search_res = SportItem.query.filter_by(id=int(command)).first()
        # 我们认为search_res是一个数组，首先统计一下，然后下载pagination
        found = len(search_res)
        page = request.args.get(get_page_parameter(), type=int, default=1)
        
        per_page = int(request.args.get('per_page', default = 20)) # 这样可以整除
        # print(found, type(page), type(per_page))
        # 要传进template的代码
        res = [single for single in search_res[(page - 1) * per_page: page * per_page]]
        # res = [[each for each in res[i * 2: i * 2 + 2]] for i in range(per_page // 2)]

        pagination = Pagination(found = found, page = page, search = True, total = found, per_page = per_page, bs_version=4)
        return render_template('result.html', res=res, keyword = form.data['content'], pagination = pagination)
    else:
        print(form.errors, "错误信息")
    return render_template("index.html", form=form)

@main.route('/upload', methods = ['GET', 'POST'])
def upload():
    print(request.method)

    form = UploadForm()
    if form.validate_on_submit():
        # f = form.img_file.data
        print("Here")
        f = request.files['img_file']
        filename =random_filename(f.filename)
        print(filename)
        
        f.save(os.path.join(file_path, filename))
        
        # session['filenames'] = [filename]
        # search_res = [SportItem.query.filter_by(id=i).first() for i in all_id]
        return render_template('index.html')
        # return redirect(url_for('img_result', filename = filename))
    print("Here")
    return render_template("upload.html", form=form)


@main.route('/img_result', methods=['GET'])
def img_result():
    filename = request.args.get('filename')
    print(filename)
    print('____________________________')
    page = request.args.get(get_page_parameter(), type=int, default=1)
    
    per_page = int(request.args.get('per_page', default = 20)) # 这样可以整除
    all_id = query(os.path.join(file_path, filename))
    search_res = [SportItem.query.filter_by(id=i).first() for i in all_id]
    res = [single for single in search_res[(page - 1) * per_page: page * per_page]]
    found = len(search_res)
    pagination = Pagination(found = found, page = page, search = True, total = found, per_page = per_page, bs_version=4)
    return render_template('result.html', res=res, keyword = "", pagination = pagination)


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
    search_res = es_fp.ES_keywords("title", item_item.Name)[1:7]
    search_res = search_res + [{'id': 0, 'title': '商品示例', 'url': '/', 'image_url': ['http://img3m9.ddimg.cn/74/17/1338216239-1_u_8.jpg'],
                                'keywords': [], 'brand': '暂无', 'brand_id': 0, 'score': 0, 'price': 0, 'hotword': ''}] * (6-len(search_res))
    recommand = [search_res, brand_res]

    return render_template("item.html", item_detail=item_detail, recommand=recommand, item=item_item)


@main.route("/wordcloudChart")
def get_wordcloud_chart():
    id = request.args.get('id')
    id = int(id)
    c = wordcloud_base(id)
    return c.dump_options_with_quotes()
        
