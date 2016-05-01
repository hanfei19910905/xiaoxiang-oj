from flask import Blueprint

download = Blueprint('download', __name__)

from . import views
