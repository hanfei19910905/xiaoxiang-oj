from flask import send_from_directory, flash, render_template, redirect
from flask_login import login_required, current_user
from . import download
from ..models import Submission, Problem
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


@download.route('/show/<sid>')
@login_required
def code_show(sid):
    print('come!')
    sub = Submission.query.filter_by(id = sid).first()
    if sub is not None:
        if not current_user.is_admin or current_user.id != sub.user.id:
            flash('你没有权限查看这个提交！')
            return redirect('/status')
        p_list = []
        id = 0
        print('source type', sub.source)
        if sub.source[-2:] == 'py':
            print('first')
            filename ='source.py'
            path = os.path.join(app.config['UPLOAD_FOLDER'], 'submission', sid, filename)
            fd = open(path, 'r')
            content = fd.read()
            return render_template('code_view.html', code_list = [['source.py', '0', content]], user = sub.user, prob = sub.prob)
        else:
            print('second')
            for parent, dir, filenames in os.walk(os.path.join(app.config['UPLOAD_FOLDER'], 'submission', sid, 'problem')):
                print('parent', parent)
                for filename in filenames:
                    print('filename: ', filename)
                    if filename[-3:] == '.py':
                        path = os.path.join(app.config['UPLOAD_FOLDER'], 'submission', sid, 'problem', filename)
                        fd = open(path, 'r')
                        content = fd.read()
                        id+=1
                        p_list.append([filename, str(id), content])
                break
            return render_template('code_view.html', code_list = p_list, user = sub.user, prob = sub.prob)
    flash('没有找到这个提交!')
    return redirect("/admin/submission/")


@download.route('/show_prob/<pid>')
@login_required
def code_prob(pid):
    prob = Problem.query.filter_by(id = pid).first()
    print("Get!")
    if prob is not None:
        return render_template('show_prob.html',prob = prob)
    flash('没有找到这个提交!')
    return redirect("/admin/problem/")
