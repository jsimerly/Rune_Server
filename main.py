from __future__ import annotations
from network import NetworkManager
from user import UserManager
from match_maker import MatchMaker
from draft import DraftManager
import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from network import MessageType

class Server:
    def __init__(self) -> None:
        self.network = NetworkManager()
        self.user_manager = UserManager()

        self.match_maker = MatchMaker(self)
        self.draft_manager = DraftManager(self)
        self.game_manager = 0

    async def update(self):
        while True:
            messages = self.network.read_queue()
            for message in messages:
                if message:
                    self.route_message(message)
                else:
                    print('Handle could not decode error')
            await asyncio.sleep(0)

    async def run(self):
        # Start the server and the update loop concurrently.
        server_task = asyncio.create_task(self.network.start('localhost', 8765))
        update_task = asyncio.create_task(self.update())
        await asyncio.gather(server_task, update_task)

    def route_message(self, message_tuple: MessageType):
        encoded_message, websocket = message_tuple
        message = self.network.decode_json(encoded_message)

        if message['type'] == 'login':
            self.user_manager.handle_message(message, websocket)
            return
        
        if message['user']:
            user_obj = self.user_manager.get_user(message['user']['username'])
            message['user'] = user_obj

        if message['type'] == 'match_making':
            self.match_maker.handle_message(message)
            return

if __name__ == "__main__":
    server = Server()
    asyncio.run(server.run())
