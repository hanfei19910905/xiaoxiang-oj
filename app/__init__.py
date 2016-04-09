from flask import Flask
from flask_bootstrap import Bootstrap
from flask_peewee.db import Database
from flask_login import LoginManager

from config import config

bootstrap = Bootstrap()

app = Flask(__name__)
app.config.from_object(config['default'])
db = Database(app)
bootstrap.init_app(app)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)
login_manager.init_app(app)

from .prob import prob as prob_blueprint
app.register_blueprint(prob_blueprint)
