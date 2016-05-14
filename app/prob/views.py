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
    return render_template('prob_list.html', plist=plist, active='problem')


def checkValid(hid, pid):
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
                    return redirect(request.args.get('next') or url_for("main.index")), False, problem, homework
            break
    return None, True, problem, homework


def clear_env():
    current_user.sub_id = -1
    db.session.commit()


@prob.route('/problem_set/<hid>/<pid>', methods=['GET', 'POST'])
@login_required
def prob_view(hid, pid):
    if request.method  == 'GET':
        return prob_view_get(hid, pid)
    else:
        print('fuck!!')
        files = request.files
        print(request.files)
        key = ""
        for _ in files.keys():
            key = _
        value = files[key] # this is a Werkzeug FileStorage object
        if 'Content-Range' in request.headers:
            if key == 'Result':
                id = current_user.sub_id
                if id != -1:
                    range_str = request.headers['Content-Range'].split(" ")[1]
                    left, right_str = range_str.split('-')
                    right, all = right_str.split('/')
                    left, right, all = int(left), int(right), int(all)
                    print(left, right, all)
                    submission_path = os.path.join(app.config['UPLOAD_FOLDER'], 'submission', str(id), 'result.csv')
                    if left == 0: # clear path
                        try :
                            os.remove(submission_path)
                        except:
                            pass
                    with open(submission_path, 'ab') as f:
                        f.write(value.stream.read())
                    if left + 1 == all:
                        sub = Submission.query.filter_by(id = id).first()
                        if sub is None:
                            flash('unkown error!')
                            return redirect(request.args.get('next') or url_for("main.index"))
                        problem = sub.problem
                        #todo: check if it is a zip file.
                        sandbox_client.call(id, os.path.join(app.config['UPLOAD_FOLDER'], 'submission', str(id), 'result.csv'), \
                                            os.path.join(app.config['UPLOAD_FOLDER'], problem.data.test2), \
                                            os.path.join(app.config['UPLOAD_FOLDER'], problem.judge.code))

                        flash("提交成功")
                        clear_env()
                        return redirect(url_for('prob.status'))
                    else:
                        return ("", 200)
                err = '未知错误！'
            else:
                err = '源文件大小不可以超过1MB!!'
            flash(err)
            clear_env()
            return redirect(url_for('prob.prob_view', hid = hid, pid = pid))
        elif key == "Source":
            # first check
            result, ok, problem, homework = checkValid(hid, pid)
            if not ok :
                return result
            form = SubmitForm()
            if form.validate_on_submit() and problem is not None and homework is not None:
                if current_user.sub_id != -1:
                    flash("请等一会再提交！")
                    return redirect(request.args.get('next') or url_for("main.index"))
                src_ext = value.filename.rsplit('.', 1)[-1]
                if homework.begin_time < datetime.datetime.now() < homework.end_time:
                    sub = Submission(user_id = current_user.id, h_id = hid, prob_id = pid, source = src_ext, result = "", time = datetime.datetime.now(), status = 'pending')
                else:
                    flash('the homework is out of date!')
                    return redirect(request.args.get('next') or url_for("main.index"))
                db.session.add(sub)
                db.session.commit()
                try:
                    submission_path = os.path.join(app.config['UPLOAD_FOLDER'], 'submission', str(sub.id))
                    os.makedirs(submission_path)
                    print (submission_path)
                    if src_ext =='py':
                        value.save(os.path.join(submission_path, 'source.py'))
                    else:
                        value.save(os.path.join(submission_path, value.filename))
                        cmd= "unzip %s -d %s" % (os.path.join(submission_path, value.filename), submission_path)
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
                current_user.sub_id = sub.id
                db.session.commit()
                return ("", 200)
        else:
            id = current_user.sub_id
            if id != -1:
                sub = Submission.query.filter_by(id = id).first()
                if sub is None:
                    flash('unkown error!')
                    return redirect(request.args.get('next') or url_for("main.index"))
                problem = sub.problem
                submission_path = os.path.join(app.config['UPLOAD_FOLDER'], 'submission', str(id), 'result.csv')
                value.save(submission_path)
                sandbox_client.call(id, os.path.join(app.config['UPLOAD_FOLDER'], 'submission', str(id), 'result.csv'), \
                                    os.path.join(app.config['UPLOAD_FOLDER'], problem.data.test2), \
                                    os.path.join(app.config['UPLOAD_FOLDER'], problem.judge.code))

                flash("提交成功")
                clear_env()
                return redirect(url_for('prob.status'))
            flash("未知错误")
            clear_env()
            return redirect(url_for('prob.prob_view', hid = hid, pid = pid))


def prob_view_get(hid, pid):
    hid = int(hid)
    pid = int(pid)
    result, ok, problem, homework = checkValid(hid, pid)
    if not ok:
        return result
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
        return render_template('prob_view.html', problem=problem, form=form, hid=-1, data=problem.data, active='problem')
    return render_template('prob_view.html', problem=problem, form=form, hid=hid, data=problem.data, active='homework')


@prob.route('/status')
@login_required
def status():
    submission_set = Submission.query.filter_by(user_id = current_user.get_id()).order_by(Submission.id.desc()).all()
    return render_template("status.html", slist = submission_set, active='status')
