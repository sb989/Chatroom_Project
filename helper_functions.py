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
        
def getSupportedLanguages(client, parent):
    try:
        supportedLangs = client.get_supported_languages(parent=parent)
        if(len(supportedLangs.languages)>0 ):
            return supportedLangs
        return None
    except:
        return None
    
def getMessageLanguage(client, parent, message):
    try:
        lang = client.detect_language(
        content=message,
        parent=parent,
        mime_type="text/plain",  
        )
        
        if(len(lang.languages)>0):
            lang=lang.languages[0].language_code
            return lang
        return None
    except:
        return None

def translateFromSourceToTarget(client,parent,sourceLang,targetLang,message):
    try:
        translatedMess = client.translate_text(
            request={
                "parent": parent,
                "contents": [message],
                "mime_type": "text/plain",
                "source_language_code": sourceLang,
                "target_language_code": targetLang,
            }
        )
        if(len(translatedMess.translations) > 0):
            translatedMess = translatedMess.translations[0].translated_text
            return translatedMess
        return None
    except:
        return None

        
def translateToRandomLang(client, parent,message):
    supportedLangs = getSupportedLanguages(client, parent)
    if(supportedLangs!=None):
        numSupportedLangs = len(supportedLangs.languages)
        targetLang = supportedLangs.languages[random.randint(0,numSupportedLangs-1)]
        targetLang = targetLang.language_code
        sourceLang = getMessageLanguage(client,parent,message)
        if(sourceLang!=None):
            translatedMess = translateFromSourceToTarget(client,parent,sourceLang,targetLang,message)
            if(translatedMess!=None):
                return translatedMess
    
    return None

