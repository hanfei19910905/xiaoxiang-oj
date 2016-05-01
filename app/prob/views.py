#!/usr/bin/env python
# coding=utf-8

from flask import render_template, redirect, url_for, flash, request
from . import prob, sandbox_client
from .. import app, db
from .forms import SubmitForm
from ..models import Problem, Submission
from flask_login import login_required, current_user
import datetime, os


@prob.route('/problem_set') 
def prob_set():
    plist = Problem.query.order_by(Problem.id).all()
    return render_template('prob_list.html', plist=plist)


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
            print ('assgin')
            homework = home
    form = SubmitForm()
    print(problem, homework, home_list)
    if form.validate_on_submit() and problem is not None and homework is not None:
        source = form.source.data
        if len(source.filename) < 3 or source.filename[-3:] != '.py' :
            flash('the source file should end with .py, but yours are %s' % source.filename)
            return redirect(request.args.get('next') or url_for("main.index"))
        result = form.result.data
        if len(result.filename) < 4 or result.filename[-4:] != '.csv' :
            flash('the source file should end with .csv, but yours are %s' % result.filename)
            return redirect(request.args.get('next') or url_for("main.index"))
        sub = Submission(user_id = current_user.id, h_id = hid, prob_id = pid, source = source.filename, result = result.filename, time = datetime.datetime.now())
        db.session.add(sub)
        db.session.commit()
        try:
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'submission', str(sub.id)))
            source.save(os.path.join(app.config['UPLOAD_FOLDER'], 'submission', str(sub.id), 'source.py'))
        except os.error:
            flash('save source file failed!')
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
        return redirect(url_for("prob.status"))

    else:
        flash('something wrong!')
        print("not valid!")
    return render_template('prob_view.html', problem=problem, form = form, hid = -1)


@prob.route('/status')
@login_required
def status():
    submission_set = Submission.query(user = current_user.get_id()).order_by(Submission.id.desc())
    return render_template("status.html", slist = submission_set, cuid = int(current_user.get_id()))

# @prob.route('/status/<sid>/code')
# @login_required
# def code_view(sid):
#     submission = Submission.select().where(Submission.id == sid).get()
#     return render_template("code_view.html", submit=submission)