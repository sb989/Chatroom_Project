from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models 
import random
import datetime
from helper_functions import generate_username

app = flask.Flask(__name__)
dotenv_path = join(dirname(__file__), '../keys/sql.env')
load_dotenv(dotenv_path)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

sql_user = os.getenv('SQL_USER')
sql_pwd = os.getenv('SQL_PASSWORD')
dbuser = os.getenv('USER')

database_uri = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.app = app


@socketio.on('new message')
def new_message(data):
    print("New Message!")
    sender = data['sender']
    dt = data['datetime']
    message = data['message']
    dt = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S.%f')
    msg = models.Message(dt,sender,message)
    db.session.add(msg)
    db.session.commit()
    table = models.Message.query.all()
    socketio.emit('new_message',{
        'message':message,
        'dt':str(dt),
        'sender':sender
        },broadcast=True)
    db.session.close()
@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    print(" client(s) are now connected")
    msgs = models.Message.query.all()
    username = generate_username(db)
    print(username)
    user = models.Username(username)
    db.session.add(user)
    db.session.commit()
    message = {'messages':[]}
    for msg in msgs:
        message['messages'].append({'m':msg.message,'sender':msg.username,'dt':str(msg.date_time)})
    socketio.emit('connected', {
        'test': 'Connected',
        'msgs':message,
        'username':username
    })
    db.session.close()
@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')
    db.session.close()
@app.route('/')
def index():
    models.db.create_all()
    
    db.session.commit()
    db.session.close()
    return flask.render_template("index.html")
    
    
if __name__ == '__main__':
    socketio.run(app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
