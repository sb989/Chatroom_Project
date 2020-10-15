import random
import sqlalchemy

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
    'disagreeable'
    ]
    
nouns = [
    'hippo',
    'bee',
    'giraffe',
    'toaster',
    'cereal',
    'car',
    'bus',
    'lemur',
    'bird',
    'monkey'
    ]

# def generateUsername(sessionLocal):
#     db = sessionLocal()
#     username = (adjectives[random.randint(0,19)] 
#                 + '_'
#                 +nouns[random.randint(0,9)])

#     try:
#         dup = db.query(
#             models.Username).filter(
#             models.Username.username == username
#             ).first(
#             )
#         if dup == None:
#             user = models.Username(email,name,pic)
#             db.add(user)
#             db.commit()
#             db.close()
#         return username
#     except Exception as e:
#         print('error',e)
#         db.close()
#         return ''
        
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




def getSupportedLanguages(client, parent):
    try:
        supported_langs = client.get_supported_languages(parent=parent)
        if(len(supported_langs.languages)>0 ):
            return supported_langs
        return None
    except Exception as e:
        print("getSupportedLanguages error",e)
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
    except Exception as e:
        print("getMessageLanguage error",e)
        return None

def translateFromSourceToTarget(client,parent,sourceLang,targetLang,message):
    try:
        translated_mess = client.translate_text(
            request={
                "parent": parent,
                "contents": [message],
                "mime_type": "text/plain",
                "source_language_code": sourceLang,
                "target_language_code": targetLang,
                }
            )
        if(len(translated_mess.translations) > 0):
            translated_mess = translated_mess.translations[0].translated_text
            return translated_mess
        return None
    except Exception as e:
        print("translateFromSourceToTarget error",e)
        return None

        
def translateToRandomLang(client, parent,message):
    try:
        supported_langs = getSupportedLanguages(client, parent)
        if(supported_langs!=None):
            num_supported_langs = len(supported_langs.languages)
            target_lang = supported_langs.languages[
                random.randint(
                0,num_supported_langs-1)
                ]
            target_lang = target_lang.language_code
            source_lang = getMessageLanguage(client,parent,message)
            if(source_lang!=None):
                translated_mess = translateFromSourceToTarget(
                    client,parent,
                    source_lang,
                    target_lang,message)
                if(translated_mess!=None):
                    return translated_mess
        
        return None
    except Exception as e:
        print("translateToRandomLang error",e)
        return None
