import json
import base64
import aiohttp

from typing import Optional
from events import Events
from aiohttp_sse_client import client as sse_client

SSE_URL = "https://gateway.octii.chat/events/subscribe/"


class SSEAPIClient(Events):
    __events__ = ('on_message', 'on_event', 'on_message_edited', 'on_message_deleted')
    def set_auth_token(self, token: str):
        try:
            self.auth_token = token
            self.user_id = json.loads(base64.urlsafe_b64decode(
                self.auth_token.split(".")[1] + "=="))['sub']
            print("SSE: Logged in with user ID",
                  self.user_id, "and token", self.auth_token)
        except Exception as e:
            raise Exception("Error storing token", e)

    async def connect(self, url: Optional[str] = None):
        if not url:
            url = SSE_URL + self.user_id

        session_timeout = aiohttp.ClientTimeout()

        async with aiohttp.ClientSession(timeout=session_timeout) as session:
            async with sse_client.EventSource(url, headers={'Authorization': self.auth_token}, session=session) as event_source:
                try:
                    async for event in event_source:
                        self.on_event(event.type, json.loads(event.data))

                        if event.type == "NEW_MESSAGE":
                            self.on_message(json.loads(event.data))
                except ConnectionError:
                    pass
