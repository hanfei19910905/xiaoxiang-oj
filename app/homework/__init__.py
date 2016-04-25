#!/usr/bin/env python
# coding=utf-8

from flask import Blueprint

homework = Blueprint('home_work', __name__)

from . import views
