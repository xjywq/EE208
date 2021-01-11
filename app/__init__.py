import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import config
from flask_cors import CORS


config_name = 'default'

app = Flask(__name__)
CORS(app, supports_credentials=True)

csrf = CSRFProtect(app)
app.config.from_object(config[config_name])
config[config_name].init_app(app)



Bootstrap(app)
db = SQLAlchemy(app)


# 附加路由和错误页面
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)
