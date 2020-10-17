import random
import sqlalchemy
import datetime
import models 
import urlvalidator
from flask_socketio import emit
from bot import Bot

def checkIfUserExists(sessionLocal,email):
    db = sessionLocal()
    try:
        dup = db.query(
            models.Username).filter(
            models.Username.email == email
            ).first(
            )
        db.close()
        if dup == None:
            return False
        else:
            return True
    except Exception as e:
        print("checkIfUserExists error",e)
        return False

def createNewUserEntry(sessionLocal,email,name,pic):
    db = sessionLocal()
    user = models.Username(email,name,pic)
    db.add(user)
    db.commit()
    db.close()



def determineMessageType(message):
    try:
        temp_message = "https://"
        if(message.startswith(temp_message)):
           temp_message = ''
        temp_message += message
        urlvalidator.validate_url(temp_message)
        
        if(message.endswith('.png')
            or message.endswith('.jpg') 
            or message.endswith('.jpeg') 
            or message.endswith('.gif')):
            
            return 'img'
        else:
            return 'link'
    except urlvalidator.ValidationError:
        return 'text'
    

