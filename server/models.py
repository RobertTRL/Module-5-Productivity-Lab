from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields

from config import db, bcrypt

"""

User model   
    -> id integer
    -> username string unique not null
    -> password_hash string not null

Notes model 
    -> id integer
    ->  title string not null
    -> content string
    -> user_id integer not null
    -> created_at date not null

"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)

class Notes(db.Model):
    pass