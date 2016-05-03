from flask import send_from_directory, flash
from flask_login import login_required
from . import download
from ..models import Submission
from .. import app, admin_required
import os


@download.route('/data/<filename>')
@login_required
def download_data(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'data'), filename)


@download.route('/secret/<filename>')
@login_required
@admin_required
def download_sec(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'secret'), filename)


@download.route('/judge/<filename>')
@login_required
@admin_required
def download_judge(filename):
    print('filename', filename)
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'judge'), filename)


@download.route('/submission/<sid>/<filename>')
@login_required
def download_sub(sid, filename):
    sub = Submission.query.filterby(id = sid)
    if sub is not None:
        return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'submission', sid), filename)
    flash('没有找到这个提交!')
