from __future__ import annotations
from typing import Callable, Any, TYPE_CHECKING
import websockets
import asyncio
import json

if TYPE_CHECKING:
    from user import User

class NetworkManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(NetworkManager, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance
    
    def __init__(self):
        if self.__initialized:
            return        

        self.__initialized = True
        self.clients = set()
        self.message_queue = []

    async def start(self, host, port):
        server = await websockets.serve(self.handle_connection, host, port)
        print(f"Server started on {host}:{port}")
        await server.wait_closed()

    async def handle_connection(self, websocket, path):
        self.clients.add(websocket)
        try:
            await self.listen_for_messages(websocket)
        finally:
            self.clients.remove(websocket)

    async def listen_for_messages(self, websocket):
        for messages in websocket:
            self.message_queue.append(messages)

    def send_json_message(self, user: User, type: str, serialized_data: dict):
        asyncio.create_task(self._send_message(user, type, serialized_data))

    async def _send_message(self, user: User, type: str, serialized_data: dict):
        message = json.dumps({
            'type': type,
            'data': serialized_data,
        })
        if user.websocket in self.clients:
            await user.websocket.send(message)

    def read_queue(self) -> list[Any]:
        messages = self.message_queue.copy()
        self.message_queue.clear()
        return messages


    

    