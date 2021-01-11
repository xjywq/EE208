from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config

config_name = 'default'

app = Flask(__name__)
app.config.from_object(config[config_name])
config[config_name].init_app(app)
Bootstrap(app)
db = SQLAlchemy(app)


# 附加路由和错误页面
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)
