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

sys.path.insert(1, join(dirname(__file__), "../"))
from bot import Bot
import helper_functions as hf
import bot_helper_functions as bhf
import server_comms
import models

project_id = 1
image_id = 1
google_json = 1


dotenv_path = join(dirname(__file__), "../keys/sql.env")

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
DT_NOW = datetime.strptime("2020-10-15 13:57:02.043000", "%Y-%m-%d %H:%M:%S.%f")
TYPE = "type"
REPLY = "reply"
ERR_MSG = "err_msg"
SID = "sid"
IMG = "img"
LANG = "lang"
RESPONSE = "response"


class MockUser:
    email = ""
    name = ""
    img = ""

    def __init__(self, email, name, pic):
        self.email = email
        self.name = name
        self.pic = pic

    def __repr__(self):
        return "%s %s %s" % (self.email, self.name, self.pic)


class MockMessage:
    dt = ""
    email = ""
    message = ""
    msg_type = ""

    def __init__(self, dt, email, message, msg_type):
        self.date_time = dt
        self.email = email
        self.message = message
        self.msg_type = msg_type


class MockedUnitTests(unittest.TestCase):
    def setUp(self):
        harry = MockUser("harry@gmail.com", "harry", "banana.png")
        bobby = MockUser("bob@gmail.com", "bobby", "apple.png")

        self.mock_users = [harry, bobby]
        message1 = MockMessage(DT_NOW, harry.email, "hi", "text")
        message2 = MockMessage(DT_NOW, bobby.email, "hey", "text")
        message3 = MockMessage(DT_NOW, bobby.email, "hey", "text")

        self.mock_messages = [message1, message2, message3]

        self.sc = server_comms.ServerComms(
            database_uri, project_id, image_id, google_json
        )

        self.chatBot = Bot(project_id, image_id, google_json, "static/Robot.png")

        self.mock_image_search_json = {
            "total": 4692,
            "totalHits": 500,
            "hits": [
                {
                    "id": 195893,
                    "pageURL": "https://pixabay.com/en/blossom-bloom-flower-195893/",
                    "type": "photo",
                    "tags": "blossom, bloom, flower",
                    "previewURL": "https://cdn.pixabay.com/photo/2013/10/15/09/12/flower-195893_150.jpg",
                    "previewWidth": 150,
                    "previewHeight": 84,
                    "webformatURL": "https://pixabay.com/get/35bbf209e13e39d2_640.jpg",
                    "webformatWidth": 640,
                    "webformatHeight": 360,
                    "largeImageURL": "https://pixabay.com/get/ed6a99fd0a76647_1280.jpg",
                    "fullHDURL": "https://pixabay.com/get/ed6a9369fd0a76647_1920.jpg",
                    "imageURL": "https://pixabay.com/get/ed6a9364a9fd0a76647.jpg",
                    "imageWidth": 4000,
                    "imageHeight": 2250,
                    "imageSize": 4731420,
                    "views": 7671,
                    "downloads": 6439,
                    "favorites": 1,
                    "likes": 5,
                    "comments": 2,
                    "user_id": 48777,
                    "user": "Josch13",
                    "userImageURL": "https://cdn.pixabay.com/user/2013/11/05/02-10-23-764_250x250.jpg",
                },
                {"id": 73424},
            ],
        }

        self.mock_image_search_json_error = self.mock_image_search_json.copy()
        self.mock_image_search_json_error.pop("totalHits")

        self.success_send_message = [
            {TAG: "connected", MESSAGE: "hello", ROOM: None},
            {TAG: "connected", MESSAGE: "hello", ROOM: 1},
        ]

        self.success_update_room_count = [
            {CHANGE: 1, COUNT: 1, RESULT: 2},
            {CHANGE: -1, COUNT: 2, RESULT: 1},
            {CHANGE: -1, COUNT: 0, RESULT: 0},
        ]

        self.failure_send_message = [
            {TAG: "connected", MESSAGE: "hello", ROOM: None},
            {TAG: "connected", MESSAGE: "hello", ROOM: 1},
        ]

        self.success_record_message = [
            {EMAIL: "r123@gmail.com", MESSAGE: "hi", MSG_TYPE: "text", DT: DT_NOW}
        ]

        self.failure_record_message = [
            {EMAIL: "r123@gmail.com", MESSAGE: "hi", MSG_TYPE: "text", DT: DT_NOW}
        ]

        self.success_received_message = [
            {
                DATA: {
                    EMAIL: "r1@gmail.com",
                    DT: str(DT_NOW),
                    MSG: "hi",
                    MSG_TYPE: "text",
                }
            }
        ]

        self.success_chatbot_response = [
            {MSG: "!! image rose", REPLY: {TYPE: "img", DATA: "rose.png"}}
        ]

        self.failure_chatbot_response = [
            {
                MSG: "!! image rose",
                DT: DT_NOW,
                REPLY: {TYPE: "img", DATA: None},
                ERR_MSG: "Bot experienced an error." "Sorry for the inconvenience",
            },
            {MSG: "!! image rose", DT: DT_NOW, REPLY: {TYPE: None, DATA: None}},
        ]

        self.success_on_connect = [{SID: 5}]

        self.success_check_if_user_exists = [
            {EMAIL: "s1@njit.edu", RESULT: False},
            {EMAIL: "harry@gmail.com", RESULT: True},
        ]

        self.failure_check_if_user_exists = [{EMAIL: "s1@njit.edu", RESULT: False}]

        self.success_create_user_entry = [
            {EMAIL: "s1@njit.edu", NAME: "sarah", IMG: "apple.png"}
        ]

        self.success_get_supported_languages = [
            {
                LANG: {"languages": [{"language_code": "af"}, {"language_code": "sq"}]},
                RESULT: {
                    "languages": [{"language_code": "af"}, {"language_code": "sq"}]
                },
            },
            {LANG: {"languages": []}, RESULT: None},
        ]

        self.failure_get_supported_languages = [
            {
                LANG: {"languages": [{"language_code": "af"}, {"language_code": "sq"}]},
                RESULT: None,
            }
        ]

        self.success_bot_image_search = [
            {
                MESSAGE: "!! image flower",
                RESPONSE: self.mock_image_search_json,
                RESULT: {
                    DATA: "https://cdn.pixabay.com/photo/2013/10/15/09/12/flower-195893_150.jpg",
                    TYPE: "img",
                },
            },
            {
                MESSAGE: "!! image flower",
                RESPONSE: self.mock_image_search_json_error,
                RESULT: {DATA: None, TYPE: "img"},
            },
        ]

        self.failure_bot_image_search = [
            {
                MESSAGE: "!! image flower",
                RESPONSE: self.mock_image_search_json,
                RESULT: {DATA: None, TYPE: "img"},
            }
        ]

    def test_record_message_success(self):
        for test in self.success_record_message:
            with patch("sqlalchemy.orm.session.Session.commit") as commit, patch(
                "sqlalchemy.orm.session.Session.add"
            ) as add, patch("sqlalchemy.orm.session.Session.close") as close:
                self.sc.recordMessage(
                    test[EMAIL], test[MESSAGE], test[MSG_TYPE], test[DT]
                )
                add.assert_called_once()
                commit.assert_called_once()
                close.assert_called_once()

    def test_record_message_failure(self):
        for test in self.failure_record_message:
            with patch("sqlalchemy.orm.session.Session.commit") as commit, patch(
                "sqlalchemy.orm.session.Session.add"
            ) as add, patch("sqlalchemy.orm.session.Session.close") as close:
                add.side_effect = SQLAlchemyError()
                self.sc.recordMessage(
                    test[EMAIL], test[MESSAGE], test[MSG_TYPE], test[DT]
                )
                add.assert_called_once()
                self.assertRaises(SQLAlchemyError)
                commit.assert_not_called()
                close.assert_called_once()

    def test_send_message_success(self):
        for test in self.success_send_message:
            with patch("flask_socketio.SocketIO.emit") as mock_sock:
                self.sc.sendMessage(test[TAG], test[MESSAGE], test[ROOM])
                mock_sock.assert_called_once()

    def test_send_message_failure(self):
        for test in self.success_send_message:
            with patch("flask_socketio.SocketIO.emit") as mock_sock:
                mock_sock.side_effect = ConnectionRefusedError
                self.sc.sendMessage(test[TAG], test[MESSAGE], test[ROOM])
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
                self.assertEqual(result, expected)

    def test_received_message(self):
        for test in self.success_received_message:
            with patch("server_comms.ServerComms.recordMessage") as rec_mess, patch(
                "server_comms.ServerComms.sendMessage"
            ) as send_mess, patch(
                "server_comms.ServerComms.chatBotResponse"
            ) as chat_resp, patch(
                "helper_functions.determineMessageType"
            ) as dmt:
                dmt.return_value = test[DATA][MSG_TYPE]
                self.sc.receivedNewMessage(test[DATA])
                dmt.assert_called_once()
                rec_mess.assert_called_once()
                send_mess.assert_called_once()
                chat_resp.assert_called_once()

    def test_chatbot_response_success(self):
        for test in self.success_chatbot_response:
            with patch("server_comms.ServerComms.recordMessage") as rec_mess, patch(
                "server_comms.ServerComms.sendMessage"
            ) as send_mess, patch("bot.Bot.messageRead") as mess_read:
                mess_read.return_value = test[REPLY]
                self.sc.chatBotResponse(test[MSG], self.chatBot)
                rec_mess.assert_called_once()
                send_mess.assert_called_once()

    def test_chatbot_response_failure(self):
        for test in self.failure_chatbot_response:
            with patch("server_comms.ServerComms.recordMessage") as rec_mess, patch(
                "server_comms.ServerComms.sendMessage"
            ) as send_mess, patch("bot.Bot.messageRead") as mess_read, patch(
                "server_comms.ServerComms.createMessage"
            ) as create_mess, patch(
                "datetime.datetime"
            ) as dt:
                mess_read.return_value = test[REPLY]
                dt.now.return_value = test[DT]
                if test[REPLY][TYPE] == None:
                    self.sc.chatBotResponse(test[MSG], self.chatBot)
                    rec_mess.assert_not_called()
                    send_mess.assert_not_called()
                    create_mess.assert_not_called()
                elif test[REPLY][DATA] == None:
                    self.sc.chatBotResponse(test[MSG], self.chatBot)
                    rec_mess.assert_called_once()
                    send_mess.assert_called_once()
                    create_mess.assert_called_once_with(
                        test[ERR_MSG],
                        self.chatBot.name,
                        self.chatBot.name,
                        str(test[DT]),
                        "text",
                        self.chatBot.img,
                    )

    def query_messages(self, q):
        query = MagicMock()
        if repr(q) == repr(models.Message):
            query.all = mock.Mock(return_value=self.mock_messages)
        elif repr(q) == repr(models.Username):
            query.all = mock.Mock(return_value=self.mock_users)
        return query

    def test_on_connect_success(self):
        for test in self.success_on_connect:
            with patch("sqlalchemy.orm.session.Session.query") as query, patch(
                "sqlalchemy.orm.session.Session.close"
            ) as close, patch(
                "server_comms.ServerComms.sendMessage"
            ) as send_mess, patch(
                "server_comms.ServerComms.updateRoomCount"
            ) as update_room:
                query.side_effect = self.query_messages
                self.sc.onConnect(test[SID])
                self.assertEqual(query.call_count, 2)
                close.assert_called_once()
                send_mess.assert_called_once()
                update_room.assert_called_once()

    def checkIfUser(self, user):
        filter_mock = MagicMock()
        email = user.get_children()[1].value
        for user in self.mock_users:
            if user.email == email:
                filter_mock.first.return_value = True
                return filter_mock
        filter_mock.first.return_value = None
        return filter_mock

    def test_check_if_users_exists_success(self):
        for test in self.success_check_if_user_exists:
            with patch("sqlalchemy.orm.session.Session") as sessLocal:
                sessLocal.return_value.query.return_value.filter.side_effect = (
                    self.checkIfUser
                )
                result = hf.checkIfUserExists(sessLocal, test[EMAIL])
                expected = test[RESULT]
                self.assertEqual(result, expected)

    def test_check_if_users_exists_failure(self):
        for test in self.failure_check_if_user_exists:
            with patch("sqlalchemy.orm.session.Session") as sessLocal:
                sessLocal.return_value.query.side_effect = SQLAlchemyError()
                hf.checkIfUserExists(sessLocal, test[EMAIL])
                self.assertRaises(SQLAlchemyError)

    def test_create_user_entry_success(self):
        for test in self.success_create_user_entry:
            with patch("sqlalchemy.orm.session.Session") as sessLocal:
                hf.createNewUserEntry(sessLocal, test[EMAIL], test[NAME], test[IMG])
                sessLocal.return_value.add.assert_called_once()
                sessLocal.return_value.commit.assert_called_once()
                sessLocal.return_value.close.assert_called_once()

    def test_get_supported_languages_success(self):
        for test in self.success_get_supported_languages:
            with patch("google.cloud.translate." "TranslationServiceClient") as client:
                client.get_supported_languages.return_value.languages = test[LANG][
                    "languages"
                ]
                client.get_supported_languages.return_value.values = test[LANG]
                result = bhf.getSupportedLanguages(client, 1)
                if result != None:
                    result = result.values
                expected = test[RESULT]
                self.assertEqual(result, expected)

    def test_get_supported_languages_failure(self):
        for test in self.failure_get_supported_languages:
            with patch("google.cloud.translate." "TranslationServiceClient") as client:
                client.get_supported_languages.side_effect = Exception()
                result = bhf.getSupportedLanguages(client, 1)
                expected = test[RESULT]
                self.assertEqual(result, expected)
                self.assertRaises(Exception)

    def test_bot_image_search_success(self):
        for test in self.success_bot_image_search:
            with patch("bot.requests") as requests, patch("bot.random") as random:
                random.randint.return_value = 0
                requests.get.return_value.value = test[RESPONSE]
                requests.get.return_value.json.return_value = (
                    requests.get.return_value.value
                )
                result = self.chatBot.messageRead(test[MESSAGE])
                expected = test[RESULT]
                self.assertDictEqual(result, expected)

    def test_bot_image_search_failure(self):
        for test in self.failure_bot_image_search:
            with patch("bot.requests") as requests, patch("bot.random") as random:
                random.randint.return_value = 0
                requests.get.side_effect = Exception()
                result = self.chatBot.messageRead(test[MESSAGE])
                expected = test[RESULT]
                self.assertDictEqual(result, expected)
                self.assertRaises(Exception)


if __name__ == "__main__":
    unittest.main()
