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

def generate_username(db):
    username = adjectives[random.randint(0,19)] + '_'+nouns[random.randint(0,9)]
    try:
        dup = models.Username.query.filter_by(username=username).first()
        if dup == None:
            return username
        while dup != None:
            username+= str(random.randint(0,2000))
            dup = models.Username.query.filter_by(username=username).first()
            
        return username
    except:
        print('error')
        db.session.close()
        return ''
        