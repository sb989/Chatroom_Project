import os
from os.path import join, dirname
from dotenv import load_dotenv
import unittest
import sys
sys.path.insert(1,'../')
from bot import Bot


dotenv_path = join(
dirname(__file__),
"../keys/translate.env"
)
load_dotenv(dotenv_path)
dotenv_path = join(
    dirname(__file__),
    "../keys/imagesearch.env"
    )
    
load_dotenv(dotenv_path)

project_id = os.getenv("PROJECT_ID")
image_id = os.getenv("IMAGE_ID")
google_json = os.getenv("GOOGLE_JSON")

MESSAGE = "message"
BOT_COMMAND = "bot_command"
BOT_MESSAGE = "bot_message"
BOT_RESPONSE = "bot_response"
BOT_RESPONSE_TYPE = "bot_repsonse_type"
BOT_RESPONSE_DATA = "bot_response_data"
BOT_NAME = "ChatBot"


class UnmockedUnitTests(unittest.TestCase):
    
    
    
    def setUp(self):
        self.chatBot = Bot(
            project_id,image_id,
            google_json,'static/Robot.png')        
        self.success_bot_message_read_params = [
            {
                MESSAGE:"!! about",
                BOT_RESPONSE:{
                    BOT_RESPONSE_DATA:"I am {}. Use me to translate,"\
                    "send pictures, and more!".format(self.chatBot.name),
                    BOT_RESPONSE_TYPE:"text"
                }
            },
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
            },
            {
                MESSAGE:"Hello World",
                BOT_RESPONSE:{
                    BOT_RESPONSE_DATA:None,
                    BOT_RESPONSE_TYPE:None
                }
            },
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
        
    
    def test_bot_message_read_success(self):
        
            
        for test in self.success_bot_message_read_params:
            response = self.chatBot.messageRead(test[MESSAGE])
            expected = test[BOT_RESPONSE]
            self.assertEqual(expected[BOT_RESPONSE_TYPE],response["type"])
            self.assertEqual(expected[BOT_RESPONSE_DATA],response["data"])
            
if __name__ == "__main__":
    unittest.main()