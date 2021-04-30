import json
import base64
import asyncio
import requests

from typing import Optional

from .Message import Message
from .members import User
from .Community import CommunityBase
from .sse import SSEAPIClient

API_URL = "https://octii.chat"
GATEWAY_URL = "https://gateway.octii.chat"

# 5503cfc9-a4fd-428a-a970-af796ede686d


class APIClient:
    def __init__(self):
        self.auth_token = None
        self.user_id = None

    def init_sse(self):
        if not (self.auth_token and self.user_id):
            raise Exception(
                "Cannot initialize SSE client before authenticating!")

        self.sse = SSEAPIClient()
        self.sse.set_auth_token(self.auth_token)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.sse.connect())

    def send_message(self, channel_id: str, content: str):
        return Message.load_json({
            **self.do_rest_request("/channels/" + channel_id + "/messages", "POST",
                             json.dumps({'content': content})).json(),
            'author_id': self.user_id,
            'channel_id': channel_id
        })

    def login(self, email: str, password: str):
        res = self.do_rest_request("/users/login", "POST",
                                   json.dumps({'email': email, 'password': password}))

        if res.ok:
            self.set_auth_token(res.json()['authorization'])
        else:
            raise Exception("Error authenticating with server:", res)

    def set_auth_token(self, token: str):
        try:
            self.auth_token = token
            self.user_id = json.loads(base64.urlsafe_b64decode(
                self.auth_token.split(".")[1] + "=="))['sub']
            print("Logged in with user ID", self.user_id,
                  "and token", self.auth_token)
        except Exception as e:
            raise Exception("Error storing token", e)

    def do_rest_request(self, path: str, method: str = "GET", data: Optional[str] = None, gateway: bool = True, *, headers: any = {}):
        headers = {
            'Authorization': self.auth_token,
            'Content-Type': "application/json;charset=UTF-8",
            **headers
        }
        url = (GATEWAY_URL if gateway else API_URL) + path

        return requests.request(method, url, headers=headers, data=data)

    def fetch_user(self, user_id: str):
        return User.load_json(self.do_rest_request("/users/" + user_id).json())

    def fetch_message(self, message_id: str):
        return Message.load_json(self.do_rest_request("/messages/" + message_id).json())

    def get_communities(self, user_id: str):
        array = self.do_rest_request("/users/" + user_id + "/members").json()
        community_objects = []

        for json_data in array:
            community_objects.append(CommunityBase.load_json(json_data))

        return community_objects

    def delete_message(self, message_id: str):
        self.do_rest_request("/messages/" + message_id, "DELETE")

    def get_messages(self, channel_id: str):
        array = self.do_rest_request("/channels/" + channel_id + "/messages").json()
        message_objects = []

        for json_data in array:
            message_objects.append(Message.load_json(json_data))

        return message_objects

    def upload_file(self, filename: str, file_contents: bytes):
        return requests.post("https://innstor.innatical.com/", files={ 'file': (filename, file_contents, 'image/jpeg') }).json()['file']