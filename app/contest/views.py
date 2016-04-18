#!/usr/bin/env python
# coding=utf-8

from flask import render_template, redirect, request, url_for, flash
from . import contest
from ..prob import prob
from ..models import Contest, Problem, Submission, User

@contest.route('/clist')
def clist_view():
    clist = None
    try:
        clist = Contest.select()
    except ContestDoesNotExist:
        pass
    return render_template('contest_list.html', clist=clist)

@contest.route('/cview/<cid>')
def contest_view(cid):
    plist = None
    contest = Contest.select().where(Contest.id==cid).get()
    try:
        plist = Problem.select().where(Problem.contest == cid)
    except ProblemDoesNotExist:
        pass
    return render_template('contest_view.html', plist=plist, contest=contest)

@contest.route('/cview/<cid>/status')
def status(cid):
    submission_set = Submission.select().where(Submission.contest == cid).order_by(Submission.id.desc())
    contest = Contest.select(Contest.id == cid).get()
    return render_template('status.html', slist=submission_set, contest=contest)

@contest.route('/cview/<cid>/ranklist')
def rank_view(cid):
    submission_set = Submission.select().where(Submission.contest == cid).order_by(Submission.id.desc())
    problem_set = Problem.select().where(Problem.contest == cid).order_by(Problem.show_id.desc())
    status_map = {0: 'Judging', 1: 'Accepted', 2: 'Wrong Answer', -1: 'Others'}
    stas = dict()
    for sub in submission_set:
        user = User.select().where(User.id == sub.user).get()
        if user.name not in stas:
            stas[user.name] = {'ac_cnt': 0, 'time': 0, 'prob': dict()}
            for prob in problem_set:
                stas[user.name]['prob'][prob.show_id] = ''
        problem = Problem.select().where(Problem.id == sub.prob).get()
        stas[user.name]['prob'][problem.show_id] = status_map[sub.status]
        if sub.status == 1:
            stas[user.name]['ac_cnt'] += 1

    rank = sorted(stas.items(), key=lambda d:(d[1]['ac_cnt'], -d[1]['time']), reverse=True)

    return render_template('ranklist.html', res=rank, plist=problem_set)