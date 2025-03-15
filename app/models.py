from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    balance = db.Column(db.Float, default=1000)
    
    # user is host or client
    games_hosted = db.relationship('Game', foreign_keys='Game.host_id', backref='host', lazy='dynamic')
    games_joined = db.relationship('Game', foreign_keys='Game.client_id', backref='client', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    host_role = db.Column(db.String(10))  # row or col
    matrix = db.Column(db.String(64))      # stored as a json string
    incentive = db.Column(db.Float)

    host_choice = db.Column(db.String(10))
    client_choice = db.Column(db.String(10))
    state = db.Column(db.String(20), default='offering')  # 'offering' or 'completed'
    
    def get_matrix(self):
        return json.loads(self.matrix)
    
    def set_matrix(self, matrix):
        self.matrix = json.dumps(matrix)
    
    def __repr__(self):
        return '<Game {}>'.format(self.id)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    block_number = db.Column(db.Integer)
    tx_type = db.Column(db.String(20))  # "game_offer", "game_join", "game_result"
    host_user = db.Column(db.String(64))
    client_user = db.Column(db.String(64), nullable=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    details = db.Column(db.Text)  # json string 

    def __repr__(self):
        return '<Transaction {}>'.format(self.id)

class HostOffering(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    host_role = db.Column(db.String(10))  #"row or col
    matrix = db.Column(db.String(64))
    incentive = db.Column(db.Float)

    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    
    def get_matrix(self):
        return json.loads(self.matrix)
    
    def set_matrix(self, matrix):
        self.matrix = json.dumps(matrix)
    
    def __repr__(self):
        return '<HostOffering {}>'.format(self.id)
