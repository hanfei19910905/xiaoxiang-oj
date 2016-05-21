from flask import Flask, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_admin import Admin
from sqlalchemy.orm import sessionmaker
from config import config
from functools import wraps
import logging
from logging.handlers import RotatingFileHandler
from celery import Celery

bootstrap = Bootstrap()

app = Flask(__name__)
app.config.from_object(config['default'])
handler= RotatingFileHandler('/var/log/xiaoxiang/foo.log', backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
db = SQLAlchemy(app)
engine = db.get_engine(app)
Session = sessionmaker(bind=engine)
bootstrap.init_app(app)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'

celery = Celery(app.name, broker="amqp://guest@localhost//")
celery.conf.update(app.config)

def admin_required(view_func):
    @wraps(view_func)
    def decorator(*args, **kwargs):
        if current_user.is_admin:
            return view_func(*args, **kwargs)
        else:
            flash("你没有权限进行这个操作！")
            return redirect(url_for('main.login', next = request.url))
    return decorator


def teacher_required(view_func):
    @wraps(view_func)
    def decorator(*args, **kwargs):
        if current_user.is_teacher:
            return view_func(*args, **kwargs)
        else:
            flash("你没有权限进行这个操作！")
            return redirect(url_for('main.login', next = request.url))
    return decorator


from .main import main as main_blueprint
app.register_blueprint(main_blueprint)
login_manager.init_app(app)

from .prob import prob as prob_blueprint
app.register_blueprint(prob_blueprint)

from .homework import homework as homework_blueprint
app.register_blueprint(homework_blueprint, url_prefix='/homework')

from .download import download as download_blueprint
app.register_blueprint(download_blueprint, url_prefix='/download')

_admin = Admin(app, template_mode='bootstrap3', name='教师管理页')
from . import admin
