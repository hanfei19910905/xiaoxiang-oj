#!/usr/bin/env python
# coding=utf-8

from flask import Blueprint

contest = Blueprint('contest', __name__)

from . import views
