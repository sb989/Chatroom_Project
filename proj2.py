import os
from os.path import join, dirname
from dotenv import load_dotenv
import random
import datetime

import flask
import flask_socketio
from flask_socketio import emit
import logging
import urlvalidator

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import models

from helper_functions import checkIfUserExists,createNewUserEntry
from  bot import Bot

dotenv_path = join(
    dirname(__file__),
    "../keys/sql.env"
    )
load_dotenv(dotenv_path)


dotenv_path = join(
    dirname(__file__),
    "../keys/translate.env"
    )
load_dotenv(dotenv_path)

dotenv_path = join(
    dirname(__file__),
    "../keys/imagesearch.env"
    )
load_dotenv(dotenv_path)

connections = 0
sql_user = os.getenv("SQL_USER")
sql_pwd = os.getenv("SQL_PASSWORD")
dbuser = os.getenv("USER")
database_uri = os.getenv("DATABASE_URL")
project_id = os.getenv("PROJECT_ID")
image_id = os.getenv("IMAGE_ID")
google_json = os.getenv("GOOGLE_JSON")

engine = create_engine(
    database_uri,echo=False
    )
sessionLocal = sessionmaker(
    autocommit = False,autoflush = False,bind = engine
    )

Base = declarative_base()


app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(
    app, cors_allowed_origins = "*"
    )


@socketio.on("login")
def login(user):
    if(not checkIfUserExists(sessionLocal,user["email"])):
        createNewUserEntry(sessionLocal,user["email"],user["name"],user["pic"])
    on_connect()



@socketio.on("new message")
def new_message(data):
    print("New Message!")
    email = data["email"]
    name = data["name"]
    dt = data["datetime"]
    message = data["message"]
    msg_type = determineMessageType(data["message"])
    print(msg_type)
    img = data["img"]
    index = data["index"]
    dt = datetime.datetime.strptime(
        dt, "%Y-%m-%d %H:%M:%S.%f"
        )
    
    msg = models.Message(
        dt,email,message,msg_type
        )
    db = sessionLocal()
    db.add(msg)
    db.commit()
    db.close()

    emit(
        "new message",{
        "message":message,
        "dt":str(dt),
        "sender":name,
        "email":email,
        "msg_type":msg_type,
        "img":img,
        "index":index
        },broadcast=True
        )
    
    chatBotResponse(message)
        

def determineMessageType(message):
    try:
        urlvalidator.validate_url(message)
        if(message.endswith('.png')
            or message.endswith('.jpg') 
            or message.endswith('.jpeg') 
            or message.endswith('.gif')):
            
            return 'img'
        else:
            return 'link'
    except urlvalidator.ValidationError:
        return 'text'
    
def chatBotResponse(message):
    reply = chatBot.messageRead(message)
    dt = str(datetime.datetime.now())
    if(reply["type"]!= None):
        message = reply["data"]
        if(reply["data"] == None):
            message = "Bot experienced an error.\
                Sorry for the inconvenience"
            reply["type"] = "text"
        emit(
            "Bot",
            {
            "message":message,
            "sender":chatBot.name,
            "email":chatBot.name,
            "dt":dt,
            "msg_type":reply["type"]
            },
            broadcast=True
            )
    
        sender = chatBot.name
        message = reply["data"]
        msg_type = reply["type"]
        
        msg = models.Message(
            dt,sender,
            message,msg_type
            )
        db = sessionLocal()
        db.add(msg)
        db.commit()
        db.close()

def on_connect():
    print("Someone connected!")
    global connections
    connections += 1
    print(connections," client(s) are now connected")
    db = sessionLocal()
    msgs = db.query(
        models.Message
        ).all()
    usrs = db.query(
        models.Username
        ).all()
    message = {"messages":[]}
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
        if(i>0 and msg.email == msgs[i-1].email):
            same_or_diff_sender = "same_sender"
        message["messages"].append(
            {"m":msg.message,
            "sender":users[msg.email]["name"],
            "email":msg.email,
            "dt":str(msg.date_time),
            "msg_type":msg.msg_type,
            "img":users[msg.email]["img"],
            "same_or_diff_sender":same_or_diff_sender
            }
            )
   
    emit(
        "connected", 
        {"test": "Connected",
        "msgs":message
        }
        )
    emit(
        "room_count",
        {"count":connections}
        ,broadcast = True
        )
    db.close()
    
@socketio.on("disconnect")
def on_disconnect():
    global connections
    connections -= 1
    print ("Someone disconnected!")
    print(connections," client(s) are now connected")
    emit(
        "room_count",
        {"count":connections}
        ,broadcast = True
        )

@app.route("/")
def index():
    return flask.render_template("index.html")


if __name__ == "__main__":
    chatBot = Bot(project_id,image_id,google_json)
    db = sessionLocal()
    if(not checkIfUserExists(sessionLocal,chatBot.name)):
        createNewUserEntry(sessionLocal,chatBot.name,chatBot.name,'static/Robot.png')
    socketio.run(app,
        host = os.getenv("IP", "0.0.0.0"),
        port = int(os.getenv("PORT", 8080)),
        debug = True,
        log_output = False
        )
