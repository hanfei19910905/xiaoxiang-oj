from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib import sqla
from sqlalchemy.orm import sessionmaker
from config import config

bootstrap = Bootstrap()

app = Flask(__name__)
app.config.from_object(config['default'])
db = SQLAlchemy(app)
engine = db.get_engine(app)
Session = sessionmaker(bind=engine)
bootstrap.init_app(app)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)
login_manager.init_app(app)

#from .prob import prob as prob_blueprint
#app.register_blueprint(prob_blueprint)

from .homework import homework as homework_blueprint
app.register_blueprint(homework_blueprint, url_prefix='/homework')

# _admin = Admin(app, template_mode='bootstrap3')
# from . import admin
