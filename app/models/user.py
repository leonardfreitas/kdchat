from app import db, bcrypt
from sqlalchemy.inspection import inspect

class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(20))
    token = db.Column(db.String(400), unique=True)

    def __init__(self, username, password, token):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.token = token

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Room(db.Model):

    __tablename__ = 'roons'
    id = db.Column(db.Integer, primary_key=True)
    public_key = db.Column(db.String(400))
    token_room = db.Column(db.String(400))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', foreign_keys=user_id)

    def __init__(self, public_key, token_room, user_id):
        self.public_key = public_key
        self.token_room = token_room
        self.user_id = user_id


