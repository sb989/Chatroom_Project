import datetime

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from helper_functions import determineMessageType,\
    checkIfUserExists,createNewUserEntry

import models
from bot import Bot

class ServerComms:
    
    def updateRoomCount(self,room_count_change):
        self.room_count += room_count_change
        if(self.room_count < 0):
            self.room_count = 0
        tag = "room_count"
        message = {"count":self.room_count}
        self.sendMessage(tag,message)
        
    def createMessage(
            self,msg,name,email,
            dt,msg_type,img,index = -1,
            same_or_diff_sender = ''):
        message = {
            "msg":msg,
            "email":email,
            "name":name,
            "dt":dt,
            "msg_type":msg_type,
            "img":img,
            "index":index,
            "same_or_diff_sender":same_or_diff_sender
        }
        return message
        
    def sendMessage(self,tag,message,room=None):
        if(room == None):#when room is not included it sends to everyone
            self.socketio.emit(tag,message)
        else:
            self.socketio.emit(tag,message,room=room)
        
    def recordMessage(self,email,msg,msg_type,dt):
        db_msg = models.Message(dt,email,msg,msg_type)
        db = self.sessionLocal()
        db.add(db_msg)
        db.commit()
        db.close()
        
    def receivedNewMessage(self,data):
        email = data["email"]
        dt = data["dt"]
        dt = datetime.datetime.strptime(
            dt, "%Y-%m-%d %H:%M:%S.%f"
            )
        msg = data["msg"]
        msg_type = determineMessageType(data["msg"])
        message = data
        if(msg_type is not "link" and msg_type is not "img"):
            message["index"] = -1    
        self.recordMessage(email,msg,msg_type,dt)
        tag = "new message"
        message["dt"] = str(dt)
        message["msg_type"] = msg_type
        self.sendMessage(tag,message)
        self.chatBotResponse(msg,self.chatBot,self.sessionLocal)

    def chatBotResponse(self,message_received,chatBot,sessionLocal):
        reply = chatBot.messageRead(message_received)
        dt = str(datetime.datetime.now())
        if(reply["type"]!= None):
            msg = reply["data"]
            if(msg == None):
                msg = "Bot experienced an error.\
                    Sorry for the inconvenience"
                reply["type"] = "text"
            tag = "Bot"
            message = self.createMessage(
                msg,self.chatBot.name,
                self.chatBot.name,dt,
                reply["type"],chatBot.img)
            self.sendMessage(tag,message)
            email = chatBot.name
            msg = reply["data"]
            msg_type = reply["type"]
            self.recordMessage(email,msg,msg_type,dt)
    
    def onConnect(self,sid):
        db = self.sessionLocal()
        msgs = db.query(
            models.Message
            ).all()
        usrs = db.query(
            models.Username
            ).all()
        db.close()
        messages = {"messages":[]}
        users = {}
        for usr in usrs:
            users[usr.email] = {
                "name":usr.name,
                "img":usr.pic
                }
        size = len(msgs)
        for i in range(size):
            same_or_diff_sender = "diff_sender"
            msg = msgs[i]
            if(i > 0 and msg.email == msgs[i-1].email):
                same_or_diff_sender = "same_sender"
            name = users[msg.email]["name"]
            email = msg.email
            dt = str(msg.date_time)
            msg_type = msg.msg_type
            img = users[msg.email]["img"]
            messages["messages"].append(
                self.createMessage(
                    msg.message,name,email,
                    dt,msg_type,img,
                    same_or_diff_sender = same_or_diff_sender
                    )
                )
        tag = "connected"
        self.sendMessage(tag,messages,sid)
        self.updateRoomCount(1)
        
    def __init__(
            self,database_uri,
            project_id,image_id,
            google_json,socketio
            ):
        self.room_count = 0
        self.engine = create_engine(
            database_uri,echo=False
            )
        self.sessionLocal = sessionmaker(
            autocommit = False,autoflush = False,bind = self.engine
            )
        self.Base = declarative_base()
        self.chatBot = Bot(
            project_id,image_id,
            google_json,'static/Robot.png')
        self.socketio = socketio