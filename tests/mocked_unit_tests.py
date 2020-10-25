import sys
import os
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime
import unittest
import unittest.mock as mock
from unittest.mock import patch
from unittest.mock import MagicMock
from flask_socketio import ConnectionRefusedError
from sqlalchemy.exc import SQLAlchemyError

sys.path.insert(1,
join(dirname(__file__), '../'))
from bot import Bot
import helper_functions as hf
import server_comms
import models

project_id = 1
image_id = 1
google_json = 1


dotenv_path = join(
    dirname(__file__),
    "../keys/sql.env"
    )
    
database_uri = os.getenv("DATABASE_URL")

TAG = "tag"
MESSAGE = "message"
MESSAGE_SENT = "message_sent"
ROOM = "room"
CHANGE = "change"
COUNT = "count"
RESULT = "result"
EMAIL = "email"
NAME = "name"
MSG = "msg"
MSG_TYPE = "msg_type"
DATA = "data"
DT = "dt"
DT_NOW = datetime.strptime("2020-10-15 13:57:02.043000","%Y-%m-%d %H:%M:%S.%f")
TYPE = "type"
REPLY = "reply"
ERR_MSG = "err_msg"
SID = "sid"

class MockUser():
    email = ""
    name = ""
    img = ""
    def __init__(self,email,name,pic):
        self.email = email
        self.name = name
        self.pic = pic
    
    def __repr__(self):
        return "%s %s %s" %(self.email,self.name,self.pic)

class MockMessage():
    dt = ""
    email = ""
    message = ""
    msg_type = ""
    def __init__(self,dt,email,message,msg_type):
        self.date_time = dt
        self.email = email
        self.message = message 
        self.msg_type = msg_type
        
    
class MockedUnitTests(unittest.TestCase):
    def setUp(self):
        harry = MockUser("harry@gmail.com","harry","banana.png")
        bobby = MockUser("bob@gmail.com","bobby","apple.png")

        self.mock_users = [harry,bobby]
        message1 = MockMessage(DT_NOW,harry.email,"hi","text")
        message2 = MockMessage(DT_NOW,bobby.email,"hey","text")
        message3 = MockMessage(DT_NOW,bobby.email,"hey","text")

        self.mock_messages = [
            message1,message2,message3
        ]
        
        self.sc = server_comms.ServerComms(
            database_uri,project_id,
            image_id,google_json)
            
        self.chatBot = Bot(
            project_id,image_id,
            google_json,'static/Robot.png')   
            
            
        self.success_send_message = [
            {
                TAG :"connected",
                MESSAGE: "hello",
                ROOM:None
            },
            {
                TAG :"connected",
                MESSAGE: "hello",
                ROOM:1
            }
        ]
        
        self.success_update_room_count = [
            {
                CHANGE:1,
                COUNT:1,
                RESULT:2
            },
            {
                CHANGE:-1,
                COUNT:2,
                RESULT:1
            },
            {
                CHANGE:-1,
                COUNT:0,
                RESULT:0
            }
        ]
        
        self.failure_send_message = [
            {
                TAG :"connected",
                MESSAGE: "hello",
                ROOM:None
            },
            {
                TAG :"connected",
                MESSAGE: "hello",
                ROOM:1
            }
        ]
        
        self.success_record_message = [
            {
                EMAIL:"r123@gmail.com",
                MESSAGE:"hi",
                MSG_TYPE:"text",
                DT:DT_NOW
            }
        ]
        
        self.failure_record_message = [
            {
                EMAIL:"r123@gmail.com",
                MESSAGE:"hi",
                MSG_TYPE:"text",
                DT:DT_NOW
            }
        ]
    
        self.success_received_message = [
            {
                DATA:{
                    EMAIL:"r1@gmail.com",
                    DT:str(DT_NOW),
                    MSG:"hi",
                    MSG_TYPE:"text"
                }
            }
        ]
        
        self.success_chatbot_response = [
            {
                MSG : "!! image rose",
                REPLY:
                    {
                        TYPE:"img",
                        DATA:"rose.png"
                    }
            }
            
        ]
        
        self.failure_chatbot_response = [
            {
                MSG : "!! image rose",
                DT:DT_NOW,
                REPLY:
                    {
                        TYPE:"img",
                        DATA:None
                    },
                ERR_MSG : "Bot experienced an error."\
                    "Sorry for the inconvenience"
            },
            {
                MSG : "!! image rose",
                DT:DT_NOW,
                REPLY:
                    {
                        TYPE:None,
                        DATA:None
                    }
            }
        ]
        
        self.success_on_connect = [
            {
                SID:5
            }    
        ]
    def test_record_message_success(self):
        for test in self.success_record_message:
            with patch("sqlalchemy.orm.session.Session.commit") as commit,\
            patch("sqlalchemy.orm.session.Session.add") as add,\
            patch("sqlalchemy.orm.session.Session.close") as close:
                self.sc.recordMessage(
                    test[EMAIL],
                    test[MESSAGE],
                    test[MSG_TYPE],
                    test[DT]
                    )
                add.assert_called_once()
                commit.assert_called_once()
                close.assert_called_once()

    def test_record_message_failure(self):
        for test in self.failure_record_message:
            with patch("sqlalchemy.orm.session.Session.commit") as commit,\
            patch("sqlalchemy.orm.session.Session.add") as add,\
            patch("sqlalchemy.orm.session.Session.close") as close:
                add.side_effect = SQLAlchemyError()
                self.sc.recordMessage(
                    test[EMAIL],
                    test[MESSAGE],
                    test[MSG_TYPE],
                    test[DT]
                    )
                add.assert_called_once()
                self.assertRaises(SQLAlchemyError)
                commit.assert_not_called()
                close.assert_called_once()
                    
    def test_send_message_success(self):
        for test in self.success_send_message:
            with patch("flask_socketio.SocketIO.emit") as mock_sock:
                self.sc.sendMessage(
                    test[TAG],test[MESSAGE],
                    test[ROOM]
                    )
                mock_sock.assert_called_once()
        
    def test_send_message_failure(self):
        for test in self.success_send_message:
            with patch("flask_socketio.SocketIO.emit") as mock_sock:
                mock_sock.side_effect = ConnectionRefusedError
                self.sc.sendMessage(
                    test[TAG],test[MESSAGE],
                    test[ROOM]
                    )
                mock_sock.assert_called_once()
                self.assertRaises(ConnectionRefusedError)
                
    def test_update_room_count_success(self):
        for test in self.success_update_room_count:
            with patch("server_comms.ServerComms.sendMessage") as mock_send:
                mock_send.return_value = True
                self.sc.room_count = test[COUNT]
                self.sc.updateRoomCount(test[CHANGE])
                result = self.sc.room_count
                expected = test[RESULT]
                self.assertEqual(result,expected)
                
    def test_received_message(self):
        for test in self.success_received_message:
            with patch("server_comms.ServerComms.recordMessage") as rec_mess,\
            patch("server_comms.ServerComms.sendMessage") as send_mess,\
            patch("server_comms.ServerComms.chatBotResponse") as chat_resp,\
            patch("helper_functions.determineMessageType") as dmt:
                dmt.return_value = test[DATA][MSG_TYPE]
                self.sc.receivedNewMessage(test[DATA])
                dmt.assert_called_once()
                rec_mess.assert_called_once()
                send_mess.assert_called_once()
                chat_resp.assert_called_once()
                
    def test_chatbot_response_success(self):
        for test in self.success_chatbot_response:
            with patch("server_comms.ServerComms.recordMessage") as rec_mess,\
            patch("server_comms.ServerComms.sendMessage") as send_mess,\
            patch("bot.Bot.messageRead") as mess_read:
                mess_read.return_value = test[REPLY]
                self.sc.chatBotResponse(test[MSG],self.chatBot)
                rec_mess.assert_called_once()
                send_mess.assert_called_once()
    
    def test_chatbot_response_failure(self):
        for test in self.failure_chatbot_response:
            with patch("server_comms.ServerComms.recordMessage") as rec_mess,\
            patch("server_comms.ServerComms.sendMessage") as send_mess,\
            patch("bot.Bot.messageRead") as mess_read,\
            patch("server_comms.ServerComms.createMessage") as create_mess,\
            patch("datetime.datetime") as dt:
                mess_read.return_value = test[REPLY]
                dt.now.return_value = test[DT]
                if(test[REPLY][TYPE] == None):
                    self.sc.chatBotResponse(test[MSG],self.chatBot)
                    rec_mess.assert_not_called()
                    send_mess.assert_not_called()
                    create_mess.assert_not_called()
                elif(test[REPLY][DATA] == None):
                    self.sc.chatBotResponse(test[MSG],self.chatBot)
                    rec_mess.assert_called_once()
                    send_mess.assert_called_once()
                    create_mess.assert_called_once_with(
                        test[ERR_MSG],self.chatBot.name,
                        self.chatBot.name,str(test[DT]),
                        "text",self.chatBot.img
                        )
                        
    def query_messages(self,q):
        query = MagicMock()
        if repr(q) == repr(models.Message):
            query.all = mock.Mock(return_value = self.mock_messages)
        elif repr(q) == repr(models.Username):
            query.all = mock.Mock(return_value = self.mock_users)
        return query

    def test_on_connect_success(self):
        for test in self.success_on_connect:
            with patch("sqlalchemy.orm.session.Session.query") as query,\
            patch("sqlalchemy.orm.session.Session.close") as close,\
            patch("server_comms.ServerComms.sendMessage") as send_mess,\
            patch("server_comms.ServerComms.updateRoomCount") as update_room:
                query.side_effect = self.query_messages
                self.sc.onConnect(test[SID])
                self.assertEqual(query.call_count,2)
                close.assert_called_once()
                send_mess.assert_called_once()
                update_room.assert_called_once()
                
if __name__ == '__main__':
    unittest.main()