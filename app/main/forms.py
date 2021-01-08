from flask import Flask, render_template, request
from wtforms.fields import simple
from wtforms import Form
from wtforms import validators
from wtforms import widgets


app = Flask(__name__, template_folder="templates")


class SearchForm(Form):
    content = simple.StringField(
        label="搜索内容",
        widget=widgets.TextInput(),
        validators=[
            validators.DataRequired(message="请输入搜索内容")],
        render_kw={"class": "form-control"}  # 设置属性生成的html属性
    )
