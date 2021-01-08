from flask import render_template, session, redirect, url_for, request
from flask_paginate import Pagination, get_page_parameter

from . import main
from .forms import SearchForm

from .. import db
from ..models import SportItem


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
