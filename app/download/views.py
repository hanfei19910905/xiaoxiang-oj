from flask import send_from_directory, flash
from . import download
from ..models import Submission
from .. import app
import os


@download.route('/data/<filename>')
def download_data(filename):
    print('download!!', os.path.join(app.config['UPLOAD_FOLDER'], 'data'))
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'data'), filename)


@download.route('/secret/<filename>')
def download_sec(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'secret'), filename)


@download.route('/submission/<sid>/<filename>')
def download_sub(sid, filename):
    sub = Submission.query.filterby(id = sid)
    if sub is not None:
        return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'submission', sid), filename)
    flash('没有找到这个提交!')
