from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
import proj2


class Username(proj2.sc.Base):
    __tablename__ = "username"
    email = Column(String(120), primary_key=True)
    messages = relationship("Message")
    name = Column(String(120))
    pic = Column(Text)

    def __init__(self, email, name, pic):
        self.email = email
        self.name = name
        self.pic = pic

    def __repr__(self):
        return "%s %s %s" % (self.email, self.name, self.pic)


class Message(proj2.sc.Base):
    __tablename__ = "message"
    date_time = Column(DateTime, primary_key=True)
    email = Column(String(120), ForeignKey("username.email"), primary_key=True)
    message = Column(Text)
    msg_type = Column(String(100))

    def __init__(self, dt, email, msg, msg_type):
        self.date_time = dt
        self.email = email
        self.message = msg
        self.msg_type = msg_type

    def __repr__(self):
        return "Message: %s %s %s %s" % (
            self.date_time,
            self.email,
            self.message,
            self.msg_type,
        )


# proj2.sc.Base.metadata.create_all(bind=proj2.sc.engine)
