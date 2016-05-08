import os
from app import app
from app import models
from app import db
from flask_script import Manager
from sandbox import SandBoxService

manager = Manager(app)

@manager.command
def init_db():
    "Initial Database"
    db.drop_all()
    db.create_all()
    student = models.Role(name='student')
    db.session.add(student)
    teacher = models.Role(name='teacher')
    db.session.add(teacher)
    admin = models.Role(name='admin')
    db.session.add(admin)
    db.session.commit()
    admin_inst = models.User(email = 'admin@admin.com', name= 'admin', role_id = admin.id, password = '123456')
    db.session.add(admin_inst)
    db.session.commit()

@manager.command
def sandbox_service(ch):
    print("Arg ch",ch)
    SandBoxService.run(ch)

if __name__ == '__main__':
    manager.run()
