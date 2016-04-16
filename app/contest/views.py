#!/usr/bin/env python
# coding=utf-8

from flask import render_template, redirect, request, url_for, flash
from . import contest
from ..models import Contest

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
    return render_template('contest_view.html')