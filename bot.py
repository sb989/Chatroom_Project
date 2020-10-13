from google.cloud import translate
import random 
from helper_functions import translateToRandomLang
import requests

class Bot:
    commands = ['about','help','funtranslate',"image"]
    stringToMath = ''
    name=''
    project_id=''
    image_id=''
    
    def aboutMessage(self):
        aboutStr = 'I am {}. Use me to translate, send pictures, and more!'.format(self.name)
        return aboutStr
    
    def commandList(self):
        descriptions=[
        'Sends a short description of {} .'.format(self.name),
        'Sends a list of commands and what they do.',
        'Translates the message that follows into a random language.',
        'Returns a picture of the message that follows.'
        ]
        returnStr = ''
        for i in range(len(self.commands)):
            returnStr += '!! '+self.commands[i]+": "+descriptions[i]+'\n'
        return returnStr
        
    def funTranslate(self,message):
        err = "Error Translating. Sorry!"
        client = translate.TranslationServiceClient()
        location = "global"
        parent = f"projects/{self.project_id}/locations/{location}"
        translatedMess = translateToRandomLang(client,parent,message)
        if(translatedMess==None):
            return err
        else:
            return translatedMess
    
    def imageSearch(self,query):
        query = query.replace(' ','+')
        url = 'https://pixabay.com/api/?key={}&q={}&image_type=photo'.format(self.image_id,query)
        response = requests.get(url)
        response = response.json()
        if("totalHits" not in response):
            return None
        numResults = len(response["hits"])
        index = random.randint(0,numResults-1)
        imgUrl = response["hits"][index]["previewURL"]
        return imgUrl
    
    def unknownCommand(self,command):
        message = "Sorry. I don't recognize the command: "+ command+". To get a list of commands enter !! help."
        return message
        
    def messageRead(self,message):
        mList = message.split()
        ret = {}
        if(mList[0]!='!!'):
            ret['type']=None
            ret['data']=None
        if(mList[1] == self.commands[0]):
            ret['type']='text'
            ret['data']=self.aboutMessage()
        elif(mList[1] == self.commands[1]):
            ret['type']='text'
            ret['data']= self.commandList()
        elif(mList[1] == self.commands[2]):
            ret['type']='text'
            funMessage=' '.join(mList[2:])
            ret['data']= self.funTranslate(funMessage)
        elif(mList[1]== self.commands[3]):
            ret['type']='img'
            query = ' '.join(mList[2:])
            ret['data']= self.imageSearch(query)
        else:
            ret['type']='text'
            ret['data']= self.unknownCommand(mList[1])
        return ret
    def __init__(self,project_id,image_id,stm='!!',name='ChatBot'):
        self.stringToMath = stm
        self.name=name
        self.project_id = project_id
        self.image_id = image_id