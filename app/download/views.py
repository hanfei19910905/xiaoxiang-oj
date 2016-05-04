from flask import send_from_directory, flash, render_template, redirect
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
    sub = Submission.query.filter_by(id = sid).first()
    if sub is not None:
        return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'submission', sid), filename)
    flash('没有找到这个提交!')
    return redirect("/admin/submission/")

@download.route('/show/<sid>/<filename>')
@login_required
def code_show(sid, filename):
    sub = Submission.query.filter_by(id = sid).first()
    print("Get!")
    if sub is not None:
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'submission', sid, filename)
        fd = open(path, 'r')
        content = fd.read()
        return render_template('code_view.html', code = content, user = sub.user, prob = sub.prob)
    flash('没有找到这个提交!')
    return redirect("/admin/submission/")
