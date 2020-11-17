from flask import render_template, session, redirect, url_for, request


from . import main
from .forms import SearchForm

from .. import db
from ..models import SportItem


@main.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if request.method == "POST":
        command = request.form['command']
        return redirect(url_for('result', command=command))
    return render_template('index.html')


@main.route('/result', methods=['GET'])
def result():
    command = request.args.get('command')
    search_res = SportItem.query.filter_by(id=int(command)).first()
    return render_template('result.html', res=search_res)
