# Where we play with SQL

import uuid
import secrets
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(50), nullable = True, default='')
    email = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    character = db.relationship('Character', backref='User', lazy = True)

    def __init__(self,email,name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.name = name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self,length):
        return secrets.token_hex(length)

    def __repr__(self):
        return f'User {self.email} added to the database'

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = True, default='')
    description = db.Column(db.String(150), nullable = True, default='')
    comics_appeared_in = db.Column(db.Integer, default = False)
    super_power = db.Column(db.String(100), nullable = True, default='')
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    owner_id = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self,name,description,comics_appeared_in,super_power,date_created,owner_id, id=''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.comics_appeared_in = comics_appeared_in
        self.super_power = super_power
        self.date_created = date_created
        self.owner_id = owner_id

    def set_id(self):
        return secrets.token_urlsafe()

    def __repr__(self):
        return f"The following Hero has been added: {self.name}"

class HeroSchema(ma.Schema):
    class Meta:
        fields = ['id','name','description','comics_appeared_in', 'super_power', 'date_created', 'owner_id']

hero_schema = HeroSchema()
heros_schema = HeroSchema(many=True)
    
