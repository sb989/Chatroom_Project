from sqlalchemy import Column,Integer,String,DateTime,Text, ForeignKey
from sqlalchemy.orm import relationship
from proj2 import Base,engine

class Message(Base):
    __tablename__ = "Message"
    date_time = Column(DateTime, primary_key=True)
    username = Column(String(120),ForeignKey('Username.username'),primary_key=True)
    message = Column(Text)
    
    def __init__(self,dt,user,msg):
        self.date_time = dt
        self.username = user
        self.message = msg
    
    def __repr__(self):
        return 'Message : %s %s %s' %(self.date_time, self.username, self.message,)

class Username(Base):
    __tablename__ = "Username"
    username = Column(String(120),primary_key=True)
    messages = relationship('Message',backref='user',lazy=True)
    
    def __init__(self,user):
        self.username = user
        
    def __repr__(self):
        return '%s' %self.username
        
Base.metadata.create_all(bind=engine)