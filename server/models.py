from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields

from config import db, bcrypt

"""

User model   
    -> id integer
    -> username string unique not null
    -> password_hash string not null

Note model 
    -> id integer
    -> title string not null
    -> content string
    -> user_id integer not null
    -> created_at date not null

"""

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)

    notes = db.relationship('Note', back_populates='user')

    @hybrid_property
    def password_hash(self):
        raise AttributeError("You cannot access this attribute directly!")

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    @validates('username')
    def validate_username_uniqueness(self, key, username):
        existing = User.query.filter(User.username == username).all()

        if existing and existing.id != self.id:
            raise ValueError("Enter a unique username!")

        return username
    
class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    password_hash = fields.String(required=True, load_only=True)

    notes = fields.List(fields.Nested(lambda : NoteSchema, exclude=('user',)), dump_only=True)

class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.Date, nullable=False)

    user = db.relationship('User', back_populates='notes')

class NoteSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    content = fields.String()
    created_at = fields.Date(required=True)

    user = fields.Nested(lambda : UserSchema(exclude=('notes',)))