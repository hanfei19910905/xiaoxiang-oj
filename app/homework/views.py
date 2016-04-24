#!/usr/bin/env python
# coding=utf-8

from flask import render_template, redirect, request, url_for, flash
from . import homework
from ..prob import prob
from ..models import HomeWork, Problem, Submission, User
from peewee import DoesNotExist


@homework.route('/list')
def list_view():
    list = None
    try:
        list = HomeWork.select().order_by(HomeWork.camp)
    except DoesNotExist:
        pass
    return render_template('homework_list.html', clist=list)


# @homework.route('/cview/<cid>')
# def contest_view(cid):
#     plist = None
#     contest = TrainCamp.select().where(TrainCamp.id == cid).get()
#     try:
#         plist = Problem.select().where(Problem.contest == cid)
#     except DoesNotExist:
#         pass
#     return render_template('contest_view.html', plist=plist, contest=contest)
#
#
# @homework.route('/cview/<cid>/status')
# def status(cid):
#     submission_set = Submission.select().where(Submission.contest == cid).order_by(Submission.id.desc())
#     contest = TrainCamp.select(TrainCamp.id == cid).get()
#     return render_template('status.html', slist=submission_set, contest=contest)
#
#
# @homework.route('/cview/<cid>/ranklist')
# def rank_view(cid):
#     submission_set = Submission.select().where(Submission.contest == cid).order_by(Submission.id.desc())
#     problem_set = Problem.select().where(Problem.contest == cid).order_by(Problem.show_id.desc())
#     status_map = {0: 'Judging', 1: 'Accepted', 2: 'Wrong Answer', -1: 'Others'}
#     stas = dict()
#     for sub in submission_set:
#         user = User.select().where(User.id == sub.user).get()
#         if user.name not in stas:
#             stas[user.name] = {'ac_cnt': 0, 'time': 0, 'prob': dict()}
#             for prob in problem_set:
#                 stas[user.name]['prob'][prob.show_id] = ''
#         problem = Problem.select().where(Problem.id == sub.prob).get()
#         stas[user.name]['prob'][problem.show_id] = status_map[sub.status]
#         if sub.status == 1:
#             stas[user.name]['ac_cnt'] += 1
#
#     rank = sorted(stas.items(), key=lambda d:(d[1]['ac_cnt'], -d[1]['time']), reverse=True)
#
#     return render_template('ranklist.html', res=rank, plist=problem_set)