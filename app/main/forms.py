from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class SearchForm(FlaskForm):
    searchCommand = StringField('What do you want to search?', validators=[Required()])
    submit = SubmitField('Submit')
