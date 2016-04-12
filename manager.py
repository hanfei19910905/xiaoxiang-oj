import os
from app import app
from app import models
from flask_script import Manager

manager = Manager(app)

@manager.command
def init_db():
    "Initial Database"
    m = models.models
    if not m.User.table_exists():
        m.User.create_table()
    if not m.Contest.table_exists():
        m.Contest.create_table()
    if not m.Judge_way.table_exists():
        m.Judge_way.create_table()
    if not m.Problem.table_exists():
        m.Problem.create_table()
    if not m.Submission.table_exists():
        m.Submission.create_table()

if __name__ == '__main__':
    manager.run()
