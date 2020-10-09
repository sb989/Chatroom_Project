import flask_sqlalchemy
from proj2 import db


class Usps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120))
    
    def __init__(self, a):
        self.address = a
        
    def __repr__(self):
        return '<Usps address: %s>' % self.address 


class Message(db.Model):
    
    date_time = db.Column(db.DateTime, primary_key=True)
    username = db.Column(db.String(120),db.ForeignKey('username.username'),primary_key=True)
    message = db.Column(db.Text)
    
    def __init__(self,dt,user,msg):
        self.date_time = dt
        self.username = user
        self.message = msg
    
    def __repr__(self):
        return '<Message : %s %s %s>' %(self.date_time, self.username, self.message)

class Username(db.Model):
    username = db.Column(db.String(120),primary_key=True)
    messages = db.relationship('Message',backref='user',lazy=True)
    
    def __init__(self,user):
        self.username = user
        
    def __repr__(self):
        return '<Username %s>' %self.username