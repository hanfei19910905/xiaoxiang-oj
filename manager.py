import os
from app import app, models, db
from flask_script import Manager
from sandbox import SandBoxService
import config

manager = Manager(app)

@manager.command
def init_db():
    "Initial Database"
    #db.drop_all()
    db.create_all()
    student = models.Role(name='student')
    db.session.add(student)
    teacher = models.Role(name='teacher')
    db.session.add(teacher)
    admin = models.Role(name='admin')
    db.session.add(admin)
    db.session.commit()
    admin_inst = models.User(email='admin@admin.com', name='admin', role_id=admin.id, password='123456')
    db.session.add(admin_inst)
    db.session.commit()
    auc = models.JudgeNorm(name='auc', code='judge/auc_judge.py', owner_id=admin_inst.id)
    f1 = models.JudgeNorm(name='f1score', code='judge/f1score_judge.py', owner_id=admin_inst.id)
    rmse = models.JudgeNorm(name='rmse', code='judge/rmse_judge.py', owner_id=admin_inst.id)
    db.session.add(f1)
    db.session.add(auc)
    db.session.add(rmse)
    db.session.commit()

    pid = models.IndexSet(id = 1, set_id = -1)
    hid = models.IndexSet(id = 2, set_id = -1)
    cid = models.IndexSet(id = 3, set_id = -1)
    db.session.add(pid)
    db.session.add(hid)
    db.session.add(cid)
    db.session.commit()

@manager.command
def sandbox_service(ch):
    print("Arg ch",ch)
    SandBoxService.run(ch)

if __name__ == '__main__':

    manager.run()
