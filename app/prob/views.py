#!/usr/bin/env python
# coding=utf-8

from flask import render_template, redirect, url_for, flash, request
from . import prob, sandbox_client
from .. import app, db
from .forms import SubmitForm
from ..models import Problem, Submission, User
from flask_login import login_required, current_user
import datetime, os


@prob.route('/problem_set') 
def prob_set():
    plist = Problem.query.order_by(Problem.id).all()
    return render_template('prob_list.html', plist=plist, active = 'problem')




@prob.route('/problem_set/<hid>/<pid>', methods = ['GET', 'POST'])
@login_required
def prob_view(hid, pid):
    hid = int(hid)
    pid = int(pid)
    problem = Problem.query.filter_by(id = pid).first()
    homework = None
    home_list = problem.homework
    for home in home_list:
        print (home.id, hid)
        if int(home.id) == hid:
            homework = home
            if not homework.camp.public and not current_user.is_admin :
                valid = False
                for user in home.camp.user:
                    if user.id == current_user.id:
                        valid = True
                        break
                if not valid:
                    flash('你没有权限提交这个作业！')
                    return redirect(request.args.get('next') or url_for("main.index"))
            break
    form = SubmitForm()
    if form.validate_on_submit() and problem is not None and (homework is not None or hid == -1):
        source = form.source.data
        src_ext = source.filename.rsplit('.', 1)[-1]
        result = form.result.data
        res_ext = result.filename.rsplit('.', 1)[-1]
        if hid != -1:
            if homework.begin_time < datetime.datetime.now() < homework.end_time:
                sub = Submission(user_id = current_user.id, h_id = hid, prob_id = pid, source = src_ext, result = res_ext, time = datetime.datetime.now(), status = 'pending')
            else:
                flash('the homework is out of date!')
                return redirect(request.args.get('next') or url_for("main.index"))

        else:
            sub = Submission(user_id = current_user.id, prob_id = pid, source = src_ext, result = res_ext, time = datetime.datetime.now())

        db.session.add(sub)
        db.session.commit()
        try:
            submission_path = os.path.join(app.config['UPLOAD_FOLDER'], 'submission', str(sub.id))
            os.makedirs(submission_path)
            print (submission_path)
            if src_ext =='py':
                source.save(os.path.join(submission_path, 'source.py'))
            else:
                source.save(os.path.join(submission_path, source.filename))
                cmd= "unzip %s -d %s" % (os.path.join(submission_path, source.filename), submission_path)
                ret = os.system(cmd)
                if ret != 0 or not os.path.exists(os.path.join(submission_path, 'problem')):
                    flash('unzip failed!'  + cmd)
                    db.session.delete(sub)
                    db.session.commit()
                    return redirect(request.args.get('next') or url_for("main.index"))
        except os.error:
            flash('save source file failed! err is ', os.error.strerror)
            db.session.delete(sub)
            db.session.commit()
            return redirect(request.args.get('next') or url_for("main.index"))

        try:
            result.save(os.path.join(app.config['UPLOAD_FOLDER'], 'submission', str(sub.id), 'result.csv'))
        except os.error:
            flash('save result file failed!')
            db.session.delete(sub)
            db.session.commit()
            return redirect(request.args.get('next') or url_for("main.index"))
        sandbox_client.call(sub.id, os.path.join(app.config['UPLOAD_FOLDER'], 'submission', str(sub.id), 'result.csv'), \
                            os.path.join(app.config['UPLOAD_FOLDER'], problem.data.test2), \
                            os.path.join(app.config['UPLOAD_FOLDER'], problem.judge.code))
        return redirect(url_for("prob.status"))
    if hid == -1:
        return render_template('prob_view.html', problem=problem, form = form, hid = -1, data = problem.data, active='problem')
    return render_template('prob_view.html', problem=problem, form = form, hid = -1, data = problem.data, active='homework')


@prob.route('/status')
@login_required
def status():
    submission_set = Submission.query.filter_by(user_id = current_user.get_id()).order_by(Submission.id.desc()).all()
    return render_template("status.html", slist = submission_set, active='status')
