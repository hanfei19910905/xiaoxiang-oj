#!/usr/bin/env python
# coding=utf-8

from flask import render_template, redirect, request, url_for, flash
from . import prob
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
        Submission.create(prob = problem_id, user = current_user.get_id(), status = 0, time = datetime.datetime.now())
    else:
        print("not valid!")
    return render_template('submit.html', problem=problem, form = form)
