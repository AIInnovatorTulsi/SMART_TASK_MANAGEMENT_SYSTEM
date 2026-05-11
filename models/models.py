from extensions import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    tasks = db.relationship(
        'Task',
        backref='user',
        lazy=True
    )


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    completed = db.Column(db.Boolean, default=False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )