from flask import render_template, session, redirect, url_for, request
import json

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
        return render_template('result.html', res=search_res)
    else:
        print(form.errors, "错误信息")
    return render_template("index.html", form=form)

@main.route('/item', methods=["GET"])
def item():
    item_id = request.args.get('id')
    item_detail = SportItem.query.filter_by(id=int(item_id)).first()
    item_detail.image_url = json.loads(item_detail.image_url)
    print(item_detail.image_url)
    # Todo search
    recommand = [item_detail] * 20
    return render_template("item.html", item=item_detail, recommand=recommand)