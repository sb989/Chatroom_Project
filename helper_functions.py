import random
import flask_sqlalchemy

import models 


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

def generate_username(SessionLocal):
    db = SessionLocal()
    username = adjectives[random.randint(0,19)] + '_'+nouns[random.randint(0,9)]

    try:
        dup = db.query(models.Username).filter(models.Username.username == username).first()
        print('dup is',dup)
        if dup == None:
            user = models.Username(username)
            db.add(user)
            db.commit()
            db.close()
        return username
    except Exception as e:
        print('error',e)
        db.close()
        return ''
        