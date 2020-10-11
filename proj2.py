from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import flask_socketio
from flask_socketio import emit
import models
import random
import datetime
from helper_functions import generate_username
import logging


dotenv_path = join(dirname(__file__), '../keys/sql.env')
load_dotenv(dotenv_path)

connections = 0
sql_user = os.getenv('SQL_USER')
sql_pwd = os.getenv('SQL_PASSWORD')
dbuser = os.getenv('USER')
database_uri = os.getenv('DATABASE_URL')

engine = create_engine(database_uri,echo=False)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()


app = flask.Flask(__name__)

log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")



@socketio.on('new message')
def new_message(data):
    print("New Message!")
    sender = data['sender']
    dt = data['datetime']
    message = data['message']
    dt = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S.%f')
    msg = models.Message(dt,sender,message)
    db = SessionLocal()
    db.add(msg)
    db.commit()
    db.close()

    emit('new message',{
        'message':message,
        'dt':str(dt),
        'sender':sender
        },broadcast=True)
    
@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    global connections
    connections +=1
    print(connections," client(s) are now connected")
    db = SessionLocal()
    msgs = db.query(models.Message).all()
    username = generate_username(SessionLocal)
    print('username is ',username)
    
    message = {'messages':[]}
    for msg in msgs:
        message['messages'].append({'m':msg.message,'sender':msg.username,'dt':str(msg.date_time)})
    emit('connected', {
        'test': 'Connected',
        'msgs':message,
        'username':username
        })
    emit('room_count',{
        'count':connections
        }
    ,broadcast=True)
    db.close()
    
@socketio.on('disconnect')
def on_disconnect():
    global connections
    connections -=1
    print ('Someone disconnected!')
    print(connections," client(s) are now connected")
    emit('room_count',{
        'count':connections
        }
    ,broadcast=True)

@app.route('/')
def index():
    return flask.render_template("index.html")
    
if __name__ == '__main__':
    socketio.run(app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True,
        log_output=False
    )
