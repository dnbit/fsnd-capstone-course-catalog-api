from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Course
Has name, description and price
'''


class Course(db.Model):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    projects = db.relationship('Project', backref='course')

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

    '''
    format()
        representation of the model
    '''

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price
        }

    '''
    insert()
        inserts an item into the database
        EXAMPLE:
        course = Course(name=name, description=description, price=price)
        course.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes an item from the database
        the item must exist in the database
        EXAMPLE:
        course = Course.query.filter(Course.id == id).one_or_none()
        course.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates an item in database
        the item must exist in the database
        EXAMPLE:
        course = Course.query.filter(Course.id == id).one_or_none()
        course.name = 'New name'
        course.update()
    '''

    def update(self):
        db.session.commit()


'''
Project
Has name, age and gender
'''


class Project(db.Model):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    instructions = Column(String, nullable=False)
    course_id = Column(Integer, db.ForeignKey('courses.id'), nullable=False)

    def __init__(self, name, age):
        self.title = title
        self.instructions = instructions

    '''
    format()
        representation of the model
    '''

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'instructions': self.instructions,
        }

    '''
    insert()
        inserts an item into the database
        EXAMPLE:
        project = Project(title=title, instructions=instructions)
        project.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes an item from the database
        the item must exist in the database
        EXAMPLE:
        project = Project.query.filter(Project.id == id).one_or_none()
        project.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates an item in database
        the item must exist in the database
        EXAMPLE:
        project = Project.query.filter(Project.id == id).one_or_none()
        project.title = 'New title'
        project.update()
    '''

    def update(self):
        db.session.commit()
