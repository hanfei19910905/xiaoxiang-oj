#!/usr/bin/env python
# coding=utf-8

from flask import render_template, redirect, request, url_for, flash
from . import prob
from ..models import Problem

@prob.route('/cview/<cid>/prob/<pid>')
def prob_view(cid, pid):
    problem = Problem.select().where(Problem.contest==cid, Problem.show_id==pid).get()
    return render_template('prob_view.html', problem=problem)

@prob.route('/cview/<cid>/prob/<pid>/submit')
def submit(cid, pid):
    problem = Problem.select().where(Problem.contest==cid, Problem.show_id==pid).get()
    return render_template('submit.html', problem=problem)