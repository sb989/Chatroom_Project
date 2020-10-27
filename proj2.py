import os
from os.path import join, dirname
from dotenv import load_dotenv
import random
import datetime

import flask
import flask_socketio
from flask import request
import logging

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import models

import helper_functions as hf
from bot import Bot

# from server_comms import ServerComms
import server_comms

dotenv_path = join(dirname(__file__), "../keys/sql.env")
load_dotenv(dotenv_path)
dotenv_path = join(dirname(__file__), "../keys/translate.env")
load_dotenv(dotenv_path)
dotenv_path = join(dirname(__file__), "../keys/imagesearch.env")
load_dotenv(dotenv_path)

sql_user = os.getenv("SQL_USER")
sql_pwd = os.getenv("SQL_PASSWORD")
dbuser = os.getenv("USER")
database_uri = os.getenv("DATABASE_URL")
project_id = os.getenv("PROJECT_ID")
image_id = os.getenv("IMAGE_ID")
google_json = os.getenv("GOOGLE_JSON")


app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

sc = server_comms.ServerComms(database_uri, project_id, image_id, google_json)

socketio.init_app(app, cors_allowed_origins="*")


@socketio.on("login")
def login(user):
    if not hf.checkIfUserExists(sc.sessionLocal, user["email"]):
        hf.createNewUserEntry(sc.sessionLocal, user["email"], user["name"], user["img"])
    sid = request.sid
    sc.onConnect(sid)


@socketio.on("new message")
def newMessage(data):
    print("New Message!")
    sc.receivedNewMessage(data)


@socketio.on("disconnect")
def onDisconnect():
    sc.updateRoomCount(-1)


@app.route("/")
def index():
    return flask.render_template("index.html")


if __name__ == "__main__":
    # sc.Base.metadata.create_all(bind=sc.engine)
    models.createTable()
    if not hf.checkIfUserExists(sc.sessionLocal, sc.chatBot.name):
        hf.createNewUserEntry(
            sc.sessionLocal, sc.chatBot.name, sc.chatBot.name, sc.chatBot.img
        )
    socketio.run(
        app,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
        log_output=False,
    )
