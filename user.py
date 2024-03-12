from __future__ import annotations
from typing import TYPE_CHECKING, List
from network import NetworkManager

if TYPE_CHECKING:
    from websockets import WebSocketServerProtocol
    from network import MessageType

class User:
    def __init__(self, username: str, websocket):
        self.username: str = username
        self.websocket: WebSocketServerProtocol = websocket
    #     self.drafts: List[Draft] = []
    #     self.games: List[Game] = []

    # def add_draft(self, draft: Draft):
    #     self.drafts.append(draft)

    # def add_game(self, game: Game):
    #     self.games.append(game)

    # def remove_game(self, game: Game):
    #     self.games.remove(game)

    @property
    def serialized(self):
        return {
            'username': self.username
        }

class UserManager:
    def __init__(self) -> None:
        self.active_users: dict[str, User] = {}
        self.network = NetworkManager()

    def handle_message(self, message: MessageType, websocket: WebSocketServerProtocol):
        if message['type'] == 'login':
            username = message['data']['username']
            user = self.add_user(username, websocket)
            print(f'{username} has logged in.')
            
            message = {
                'user': user.serialized,
                'status': 'Success',
            }
            self.network.send_json_message(user=user, type='login', serialized_data=message)

    def add_user(self, username: str, websocket):
        if username in self.active_users:
            self.active_users[username].websocket = websocket
            user = self.active_users[username]
        else:
            user = self.create_user(username, websocket)
        return user
    
    def get_user(self, username):
        if username in self.active_users:
            return self.active_users[username]
        return None
    
    def create_user(self, username, websocket):
        user = User(username, websocket)
        self.active_users[username] = user
        return user

    def remove_user(self, username):
        if username in self.active_users:
            del self.active_users[username]