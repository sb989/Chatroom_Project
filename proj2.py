from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models 
import random


app = flask.Flask(__name__)
dotenv_path = join(dirname(__file__), '../keys/sql.env')
load_dotenv(dotenv_path)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

sql_user = os.environ['SQL_USER']
sql_pwd = os.environ['SQL_PASSWORD']
dbuser = os.environ['USER']

database_uri = 'postgresql://{}:{}@localhost/postgres'.format(
    sql_user, sql_pwd)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.app = app

adjectives = [
    'finicky',
    'roomy',
    'innocent',
    'zonked',
    'silent',
    'sudden',
    'nutritious',
    'outstanding',
    'rare',
    'abashed',
    'materialistic',
    'nonstop',
    'longing',
    'lacking',
    'waiting',
    'puzzling',
    'severe',
    'selfish',
    'misty',
    'disagreeable']
    
nouns = ['hippo',
    'bee',
    'giraffe',
    'toaster',
    'cereal',
    'car',
    'bus',
    'lemur',
    'bird',
    'monkey']

def generate_username():
    username = adjectives[random.randint(0,19)] + '_'+nouns[random.randint(0,9)]
    try:
        dup = models.Username.query.filter_by(username=username).first()
        print('dup is ',dup)
        if dup == None:
            print('returning ',username)
            return username
        while dup != None:
            username+= str(random.randint(0,2000))
            dup = models.Username.query.filter_by(username=username).first()
            
        return username
    except:
        print('error')
        db.session.close()
        return ''
        
@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    msgs = models.Message.query.all()
    socketio.emit('connected', {
        'test': 'Connected',
        'msgs':msgs,
        'username':generate_username()
    })
    
@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')

@app.route('/')
def index():
    models.db.create_all()
    
    db.session.commit()
    
    return flask.render_template("index.html")
    
    
if __name__ == '__main__':
    socketio.run(app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
