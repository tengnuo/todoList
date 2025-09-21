from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    avatar = db.Column(db.String(200))
    tasks = db.relationship('Task', backref='user', lazy=True)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20)) # 高中低
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default = False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))