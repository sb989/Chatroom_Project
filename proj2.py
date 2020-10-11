from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import flask_socketio
from flask_socketio import emit
import models
import random
import datetime
from helper_functions import generate_username


dotenv_path = join(dirname(__file__), '../keys/sql.env')
load_dotenv(dotenv_path)


sql_user = os.getenv('SQL_USER')
sql_pwd = os.getenv('SQL_PASSWORD')
dbuser = os.getenv('USER')
database_uri = os.getenv('DATABASE_URL')

engine = create_engine(database_uri,echo=True)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()


# db = flask_sqlalchemy.SQLAlchemy()
app = flask.Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
# app.config['SQLALCHEMY_POOL_RECYCLE'] = 20
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)
# with app.app_context():
#     db.create_all()

# db.app = app

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
    print(" client(s) are now connected")
    db = SessionLocal()
    msgs = db.query(models.Message).all()
    username = generate_username(SessionLocal)
    print('username is ',username)
    print(msgs)
    message = {'messages':[]}
    for msg in msgs:
        message['messages'].append({'m':msg.message,'sender':msg.username,'dt':str(msg.date_time)})
    emit('connected', {
        'test': 'Connected',
        'msgs':message,
        'username':username
        })
    db.close()
@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')

@app.route('/')
def index():
    return flask.render_template("index.html")
    
if __name__ == '__main__':
    socketio.run(app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
