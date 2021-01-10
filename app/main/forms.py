import os



from flask import Flask, render_template, request
from wtforms.fields import simple
from wtforms import Form
from wtforms import validators
from wtforms import widgets, SubmitField
from flask_wtf import FlaskForm
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf.file import FileAllowed, FileRequired, FileField


images = UploadSet('images', IMAGES)

class SearchForm(Form):
    content = simple.StringField(
        label="",
        widget=widgets.TextInput(),
        validators=[
            validators.DataRequired(message="请输入搜索内容")],
        render_kw={"class": "form-control"}  # 设置属性生成的html属性
    )

class UploadForm(FlaskForm):
    img_file = FileField(
        label="",
        validators=[FileRequired(), FileAllowed(images, "Image only!")]
    )
    submit = SubmitField(u'上传')
