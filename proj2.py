import os
from os.path import join, dirname
from dotenv import load_dotenv
import random
import datetime

import flask
import flask_socketio
from flask_socketio import emit
import logging

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
    sender = data["sender"]
    dt = data["datetime"]
    message = data["message"]
    msg_type = data["msg_type"]
    dt = datetime.datetime.strptime(
        dt, "%Y-%m-%d %H:%M:%S.%f"
        )
    msg = models.Message(
        dt,sender,message,msg_type
        )
    db = sessionLocal()
    db.add(msg)
    db.commit()
    db.close()

    emit(
        "new message",{
        "message":message,
        "dt":str(dt),
        "sender":sender,
        "msg_type":msg_type
        },broadcast=True
        )
    
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

    message = {"messages":[]}
    for msg in msgs:
        message["messages"].append(
            {"m":msg.message,
            "sender":msg.name,
            "dt":str(msg.date_time),
            "msg_type":msg.msg_type}
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
    if(checkIfUserExists(sessionLocal,chatBot.name)):
        createNewUserEntry(sessionLocal,chatBot.name,chatBot.name,'')
    socketio.run(app,
        host = os.getenv("IP", "0.0.0.0"),
        port = int(os.getenv("PORT", 8080)),
        debug = True,
        log_output = False
        )
