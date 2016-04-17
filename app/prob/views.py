#!/usr/bin/env python
# coding=utf-8

from flask import render_template, redirect, request, url_for, flash
from . import prob, sandbox_client
from .forms import SubmitForm
from ..models import Problem, Submission
from flask_login import login_required, current_user
import datetime


@prob.route('/cview/<cid>/prob/<pid>')
@login_required
def prob_view(cid, pid):
    problem = Problem.select().where(Problem.contest==cid, Problem.show_id==pid).get()
    return render_template('prob_view.html', problem=problem)


@prob.route('/cview/<cid>/prob/<pid>/submit', methods=['GET', 'POST'])
@login_required
def submit(cid, pid):
    problem = Problem.select().where(Problem.contest==cid, Problem.show_id==pid).get()
    form = SubmitForm()
    print(form.is_submitted())
    if form.validate_on_submit():
        problem_id = problem.id
        time_limit = problem.time_limit
        mem_limit = problem.mem_limit
        submit = Submission.create(contest = problem.contest, prob = problem_id, user = current_user.get_id(), status = 0, time = datetime.datetime.now(), source = form.source.data)
        sandbox_client.call(submit.get_id(), problem_id, time_limit, mem_limit, form.source.data)
        return redirect(url_for("prob.status"))
    else:
        print("not valid!")
    return render_template('submit.html', problem=problem, form = form)


@prob.route('/status')
@login_required
def status():
    submission_set = Submission.select().where(Submission.user == current_user.get_id()).order_by(Submission.id.desc())
    return render_template("status.html", slist = submission_set, cuid = int(current_user.get_id()))

@prob.route('/status/<sid>/code')
@login_required
def code_view(sid):
    submission = Submission.select().where(Submission.id == sid).get()
    return render_template("code_view.html", submit=submission)