import os
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime
import unittest
import sys
sys.path.insert(1,
join(dirname(__file__), '../'))
from bot import Bot
import helper_functions as hf
import server_comms
import models

project_id = 1
image_id = 1
google_json = 1
socketio = 1;


dotenv_path = join(
    dirname(__file__),
    "../keys/sql.env"
    )
    
database_uri = os.getenv("DATABASE_URL")

MESSAGE = "message"
BOT_COMMAND = "bot_command"
BOT_MESSAGE = "bot_message"
BOT_RESPONSE = "bot_response"
BOT_RESPONSE_TYPE = "bot_repsonse_type"
BOT_RESPONSE_DATA = "bot_response_data"
BOT_NAME = "ChatBot"
URL_TYPE = "url_type"

NAME = "name"
EMAIL = "email"
DT = "dt"
MSG_TYPE = "msg_type"
IMG = "img"
INDEX = "index"
SODS = "sods"
CREATED_MESSAGE = "created_message"

USERNAME_DB_PRINT = "username_db_print"
MESSAGE_DB_PRINT = "message_db_print"

DT_NOW = datetime.strptime("2020-10-15 13:57:02.043000","%Y-%m-%d %H:%M:%S.%f")

class UnmockedUnitTests(unittest.TestCase):
    
    
    
    def setUp(self):
        self.chatBot = Bot(
            project_id,image_id,
            google_json,'static/Robot.png')   
            
        self.sc = server_comms.ServerComms(
            database_uri,project_id,
            image_id,google_json)

        self.success_bot_about = [
            {
                MESSAGE:"!! about",
                BOT_RESPONSE:{
                    BOT_RESPONSE_DATA:"I am {}. Use me to translate,"\
                    "send pictures, and more!".format(self.chatBot.name),
                    BOT_RESPONSE_TYPE:"text"
                }
            }
        ]
        self.success_bot_help = [
            {
                MESSAGE:"!! help",
                BOT_RESPONSE:{
                    BOT_RESPONSE_DATA:
                        "!! about: Sends a short description"\
                            " of {} .\n".format(BOT_NAME)
                        +"!! help: Sends a list of commands"\
                            " and what they do.\n"
                        +"!! funtranslate: Translates the message "\
                            "that follows into a random language.\n"
                        +"!! image: Returns a picture of the message "\
                            "that follows.\n"
                        +"!! math: Calculates simple math equations. "\
                            "Supported symbols are +, -, /, *, (, and ).\n",
                    BOT_RESPONSE_TYPE:"text"
                }
            }
        ]
        
        self.success_bot_regular_message = [
            {
                MESSAGE:"Hello World",
                BOT_RESPONSE:{
                    BOT_RESPONSE_DATA:None,
                    BOT_RESPONSE_TYPE:None
                }
            }
            
        ]
        
        self.success_bot_undefinded_command = [
            {
                MESSAGE:"!! animals",
                BOT_RESPONSE:{
                    BOT_RESPONSE_DATA:
                    "Sorry. I don't recognize the command: animals."\
                    "To get a list of commands enter !! help.",
                    BOT_RESPONSE_TYPE:"text"
                }
            }
        ]
        
        self.success_bot_math = [
            {
                MESSAGE:"!! math 2+2",
                BOT_RESPONSE:{
                    BOT_RESPONSE_DATA: 4,
                    BOT_RESPONSE_TYPE:"text"
                }
            },
            
        ]
        
        self.failure_bot_math = [
            {
                MESSAGE:"!! math 2+",
                BOT_RESPONSE:{
                    BOT_RESPONSE_DATA: 2,
                    BOT_RESPONSE_TYPE:"text"
                }
            }
        ]
        
        self.success_determine_message_type_params = [
            {
                MESSAGE:"https://google.com",
                URL_TYPE:"link"
            },
            {
                MESSAGE:"google.com",
                URL_TYPE:"link"
            },
            {
                MESSAGE:"https://i.pinimg.com/736x/05/79/5a/05795a16b647118ffb6629390e995adb.jpg",
                URL_TYPE:"img"
            },
            {
                MESSAGE:"i.pinimg.com/736x/05/79/5a/05795a16b647118ffb6629390e995adb.jpg",
                URL_TYPE:"img"
            },
            {
                MESSAGE:"Hello World",
                URL_TYPE:"text"
            }
        ]
    
        self.failure_determine_message_type_params = [
            {
                MESSAGE:"Hello World.com",
                URL_TYPE:"link"
            }
        ]

        self.success_db_username_print = [
            {
                EMAIL:"todd@gmail.com",
                NAME:"bobby",
                IMG:"apple.png",
                USERNAME_DB_PRINT:"todd@gmail.com bobby apple.png"
            }    
        ]
        
        self.failure_db_username_print = [
            {
                
            }    
        ]
        
        self.success_db_message_print = [
            {
                DT:DT_NOW,
                EMAIL:"todd@gmail.com",
                MESSAGE:"jello",
                MSG_TYPE:"text",
                MESSAGE_DB_PRINT:"Message: {} todd@gmail.com jello text".format(DT_NOW)
            }    
        
        ]
    
    
        self.success_server_comms_create_message = [
            {
                MESSAGE:"hello",
                EMAIL:"123sesamestreet@njit.edu",
                NAME:"Oscar",
                DT:DT_NOW,
                MSG_TYPE:"text",
                IMG:"apple.png",
                CREATED_MESSAGE:{
                    "msg":"hello",
                    "email":"123sesamestreet@njit.edu",
                    "name":"Oscar",
                    "dt":DT_NOW,
                    "msg_type":"text",
                    "img":"apple.png",
                    "index":-1,
                    "same_or_diff_sender":""
                }
            },
            {
                MESSAGE:"hello",
                EMAIL:"123sesamestreet@njit.edu",
                NAME:"Oscar",
                DT:DT_NOW,
                MSG_TYPE:"text",
                IMG:"apple.png",
                INDEX:3,
                CREATED_MESSAGE:{
                    "msg":"hello",
                    "email":"123sesamestreet@njit.edu",
                    "name":"Oscar",
                    "dt":DT_NOW,
                    "msg_type":"text",
                    "img":"apple.png",
                    "index":3,
                    "same_or_diff_sender":""
                }
            },{
                MESSAGE:"hello",
                EMAIL:"123sesamestreet@njit.edu",
                NAME:"Oscar",
                DT:DT_NOW,
                MSG_TYPE:"text",
                IMG:"apple.png",
                SODS:"same_sender",
                CREATED_MESSAGE:{
                    "msg":"hello",
                    "email":"123sesamestreet@njit.edu",
                    "name":"Oscar",
                    "dt":DT_NOW,
                    "msg_type":"text",
                    "img":"apple.png",
                    "index":-1,
                    "same_or_diff_sender":"same_sender"
                }
            },{
                MESSAGE:"hello",
                EMAIL:"123sesamestreet@njit.edu",
                NAME:"Oscar",
                DT:DT_NOW,
                MSG_TYPE:"text",
                IMG:"apple.png",
                INDEX:3,
                SODS:"same_sender",
                CREATED_MESSAGE:{
                    "msg":"hello",
                    "email":"123sesamestreet@njit.edu",
                    "name":"Oscar",
                    "dt":DT_NOW,
                    "msg_type":"text",
                    "img":"apple.png",
                    "index":3,
                    "same_or_diff_sender":"same_sender"
                }
            }
            ]
    def test_bot_about_success(self):
        for test in self.success_bot_about:
            response = self.chatBot.messageRead(test[MESSAGE])
            expected = test[BOT_RESPONSE]
            self.assertEqual(expected[BOT_RESPONSE_TYPE],response["type"])
            self.assertEqual(expected[BOT_RESPONSE_DATA],response["data"])
    
    def test_bot_help_success(self):
        for test in self.success_bot_help:
            response = self.chatBot.messageRead(test[MESSAGE])
            expected = test[BOT_RESPONSE]
            self.assertEqual(expected[BOT_RESPONSE_TYPE],response["type"])
            self.assertEqual(expected[BOT_RESPONSE_DATA],response["data"])
    
    def test_bot_regular_message_success(self):
        for test in self.success_bot_regular_message:
            response = self.chatBot.messageRead(test[MESSAGE])
            expected = test[BOT_RESPONSE]
            self.assertEqual(expected[BOT_RESPONSE_TYPE],response["type"])
            self.assertEqual(expected[BOT_RESPONSE_DATA],response["data"])
    
    def test_bot_undefinded_command_success(self):
        for test in self.success_bot_undefinded_command:
            response = self.chatBot.messageRead(test[MESSAGE])
            expected = test[BOT_RESPONSE]
            self.assertEqual(expected[BOT_RESPONSE_TYPE],response["type"])
            self.assertEqual(expected[BOT_RESPONSE_DATA],response["data"])
            
    def test_bot_help_math(self):
        for test in self.success_bot_math:
            response = self.chatBot.messageRead(test[MESSAGE])
            expected = test[BOT_RESPONSE]
            self.assertEqual(expected[BOT_RESPONSE_TYPE],response["type"])
            self.assertEqual(expected[BOT_RESPONSE_DATA],response["data"])
    
    def test_bot_message_read_failure(self):
        for test in self.failure_bot_math:
            response = self.chatBot.messageRead(test[MESSAGE])
            expected = test[BOT_RESPONSE]
            self.assertEqual(expected[BOT_RESPONSE_TYPE],response["type"])
            self.assertNotEqual(expected[BOT_RESPONSE_DATA],response["data"])
    
    def test_determine_message_type_success(self):
        for test in self.success_determine_message_type_params:
            response = hf.determineMessageType(test[MESSAGE])
            expected = test[URL_TYPE]
            
            self.assertEqual(response,expected)
    
    def test_determine_message_type_failure(self):
        for test in self.failure_determine_message_type_params:
            response = hf.determineMessageType(test[MESSAGE])
            expected = test[URL_TYPE]
            
            self.assertNotEqual(response,expected)
    
    def test_server_comms_create_message(self):
        test = self.success_server_comms_create_message[0]
        response = self.sc.createMessage(
                test[MESSAGE],
                test[NAME],
                test[EMAIL],
                test[DT],
                test[MSG_TYPE],
                test[IMG]
                )
        expected = test[CREATED_MESSAGE]
        self.assertDictEqual(response,expected)
        
        test = self.success_server_comms_create_message[1]
        response = self.sc.createMessage(
                test[MESSAGE],
                test[NAME],
                test[EMAIL],
                test[DT],
                test[MSG_TYPE],
                test[IMG],
                index = test[INDEX]
                )
        expected = test[CREATED_MESSAGE]
        self.assertDictEqual(response,expected)
    
        test = self.success_server_comms_create_message[2]
        response = self.sc.createMessage(
                test[MESSAGE],
                test[NAME],
                test[EMAIL],
                test[DT],
                test[MSG_TYPE],
                test[IMG],
                same_or_diff_sender = test[SODS]
                )
        expected = test[CREATED_MESSAGE]
        self.assertDictEqual(response,expected)

        test = self.success_server_comms_create_message[3]
        response = self.sc.createMessage(
                test[MESSAGE],
                test[NAME],
                test[EMAIL],
                test[DT],
                test[MSG_TYPE],
                test[IMG],
                index = test[INDEX],
                same_or_diff_sender = test[SODS]
                )
        expected = test[CREATED_MESSAGE]
        self.assertDictEqual(response,expected)

    def test_db_username_print_success(self):
        for test in self.success_db_username_print:
            user = models.Username(
                test[EMAIL],
                test[NAME],
                test[IMG]
                )
            response = repr(user)    
            expected = test[USERNAME_DB_PRINT]
            self.assertEqual(response,expected)
    
    def test_db_message_print_success(self):
        for test in self.success_db_message_print:
            msg = models.Message(
                test[DT],
                test[EMAIL],
                test[MESSAGE],
                test[MSG_TYPE]
                )
            response = repr(msg)    
            expected = test[MESSAGE_DB_PRINT]
            self.assertEqual(response,expected)        
            
    
if __name__ == "__main__":
    unittest.main()