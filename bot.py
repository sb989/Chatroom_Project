import random 
import requests
import json
import base64

from google.cloud import translate
from google.oauth2 import service_account
from Equation import Expression
from bot_helper_functions import translateToRandomLang


class Bot:
    commands = [
        'about','help',
        'funtranslate',
        "image","math"
        ]
    string_to_match = ''
    name = ''
    project_id = ''
    image_id = ''
    google_json = ''
    img = ''
    def aboutMessage(self):
        about_str = "I am {}. Use me to translate,"\
        "send pictures, and more!".format(self.name)
        return about_str
    
    def commandList(self):
        descriptions = [
            'Sends a short description of {} .'.format(self.name),
            'Sends a list of commands and what they do.',
            'Translates the message that follows into a random language.',
            'Returns a picture of the message that follows.',
            'Calculates simple math equations. Supported symbols'\
                ' are +, -, /, *, (, and ).'
                ]
        return_str = ''
        
        for i in range(len(self.commands)):
            return_str += ('!! '
                        + self.commands[i]
                        + ": "
                        + descriptions[i]
                        + '\n'
                        )
        return return_str
        
    def funTranslate(self,message):
        err = "Error Translating. Sorry!"

        client = translate.TranslationServiceClient()
        location = "global"
        parent = f"projects/{self.project_id}/locations/{location}"
        
        translated_mess = translateToRandomLang(
            client,parent,message)
        if(translated_mess == None):
            return err
        else:
            return translated_mess
    
    def imageSearch(self,query):
        try:
            query = query.replace(' ','+')
            url = 'https://pixabay.com/api/?key={}&q={}&image_type=photo'\
                .format(self.image_id,query)
            print(url)
            response = requests.get(url)
            print(response)
            response = response.json()
            if("totalHits" not in response):
                return None
            num_results = len(response["hits"])
            index = random.randint(0,num_results-1)
            imgUrl = response["hits"][index]["previewURL"]
            return imgUrl
        except:
            return None
    
    def math(self,equation):
        result = Expression(equation[0])
        if(result() == None):
            return "Invalid Expression"
        return result()
    
    def unknownCommand(self,command):
        message = "Sorry. I don't recognize the command: {}."\
        "To get a list of commands enter !! help.".format(command)
        return message
        
    def messageRead(self,message):
        m_list = message.split()
        ret = {}
        if(m_list[0] != '!!'):
            ret['type'] = None
            ret['data'] = None
        
        elif(m_list[1] == self.commands[0]):
            ret['type'] = 'text'
            ret['data'] = self.aboutMessage()
        
        elif(m_list[1] == self.commands[1]):
            ret['type'] ='text'
            ret['data'] = self.commandList()
        
        elif(m_list[1] == self.commands[2]):
            ret['type'] ='text'
            fun_message =' '.join(m_list[2:])
            ret['data'] = self.funTranslate(fun_message)
        
        elif(m_list[1] == self.commands[3]):
            ret['type'] = 'img'
            query = ' '.join(m_list[2:])
            ret['data'] = self.imageSearch(query)
        
        elif(m_list[1] == self.commands[4]):
            ret['type'] = 'text'
            ret['data'] = self.math(m_list[2:])
       
        else:
            ret['type'] = 'text'
            ret['data'] = self.unknownCommand(m_list[1])
        return ret
    
    def __init__(
        self,project_id,image_id,
        google_json,img,
        stm = '!!',name = 'ChatBot'
        ):
        self.string_to_match = stm
        self.name = name
        self.project_id = project_id
        self.image_id = image_id
        self.google_json = google_json
        self.img = img
        