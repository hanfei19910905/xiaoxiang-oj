#!/usr/bin/env python
# coding=utf-8

from flask import render_template, redirect, request, url_for, flash
from . import contest
from ..prob import prob
from ..models import Contest
from ..models import Problem

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