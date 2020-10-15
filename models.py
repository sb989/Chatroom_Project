from sqlalchemy import Column,Integer,String,DateTime,Text, ForeignKey
from sqlalchemy.orm import relationship
from proj2 import Base,engine

class Username(Base):
    __tablename__ = "username"
    email         = Column(String(120),primary_key = True)
    messages      = relationship("Message")
    name          = Column(String(120))
    pic           = Column(Text)
    
    def __init__(self,email,name,pic):
        self.email = email
        self.name = name
        self.pic = pic
        
    def __repr__(self):
        return '%s %s' %(self.email,self.name)
        
        
class Message(Base):
    __tablename__ = "message"
    date_time     = Column(DateTime, primary_key = True)
    email          = Column(String(120),ForeignKey(
        "username.email"),
        primary_key = True
        )
    message = Column(Text)
    msg_type = Column(String(100))
    def __init__(self,dt,email,msg,msg_type):
        self.date_time = dt
        self.email = email
        self.message = msg
        self.msg_type = msg_type
    def __repr__(self):
        return "Message : %s %s %s" %(
            self.date_time, 
            self.email, 
            self.message,
            )


        
Base.metadata.create_all(bind = engine)