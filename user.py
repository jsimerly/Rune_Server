from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from websockets import WebSocketServerProtocol

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

    def serialize(self):
        return {
            'username': self.username
        }

class Database:
    def __init__(self) -> None:
        self.active_users: dict[str, User] = {}

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