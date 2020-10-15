from sqlalchemy import Column,Integer,String,DateTime,Text, ForeignKey
from sqlalchemy.orm import relationship
from proj2 import Base,engine

class Message(Base):
    __tablename__ = "Message"
    date_time     = Column(DateTime, primary_key = True)
    name          = Column(String(120),ForeignKey(
        'Username.name'),
        primary_key = True
        )
    message = Column(Text)
    msg_type = Column(String(100))
    def __init__(self,dt,name,msg,msg_type):
        self.date_time = dt
        self.name = name
        self.message = msg
        self.msg_type = msg_type
    def __repr__(self):
        return 'Message : %s %s %s' %(
            self.date_time, 
            self.name, 
            self.message,
            )

class Username(Base):
    __tablename__ = "Username"
    email         = Column(String(120),primary_key = True)
    messages      = relationship('Message',backref = 'user',lazy = True)
    name          = Column(String(120))
    pic           = Column(Text)
    
    def __init__(self,email,name,pic):
        self.email = email
        self.name = name
        self.pic = pic
    def __repr__(self):
        return '%s %s' %(self.email,self.name)
        
Base.metadata.create_all(bind = engine)