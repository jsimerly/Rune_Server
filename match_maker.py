from __future__ import annotations
from user import User
from network import NetworkManager, MessageType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Server
    from draft import Draft

class MatchMaker:
    def __init__(self, server: Server) -> None:
        self.server = server
        self.network = server.network
        self.user_1: User = None
        self.user_2: User = None

    def handle_message(self, message: MessageType):
        try:
            if message['data']['start_looking']:
                self.new_user(message['user'])
            else:
                self.remove_user(message['user'])
        except Exception as e:
            print(e)

    def new_user(self, user: User):
        if not self.user_1:
            self.user_1 = user
            self.alert_begin_looking(user)
            self.check_for_match()
            return
        if not self.user_2:
            self.user_2 = user
            self.alert_begin_looking(user)
            self.check_for_match()
            return
        
    def remove_user(self, user: User):
        if user == self.user_1:
            self.user_1 = None
            self.alert_cancel_looking(user)
        if user == self.user_2:
            self.user_2 = None
            self.alert_cancel_looking(user)

    def alert_begin_looking(self, user: User):
        info = {
            'status': 'looking_for_game'
        }
        self.network.send_json_message(user=user, type='match_making', serialized_data=info)

    def alert_cancel_looking(self, user: User):
        print('alert cancel')
        info = {
            'status': 'cancel_looking_for_game'
        }
        self.network.send_json_message(user=user, type='match_making', serialized_data=info)

    def check_for_match(self):
        if isinstance(self.user_1, User) and isinstance(self.user_2, User):
            draft_obj = self.create_draft()
            match_data = {
                'status': 'match_found',
                'map': 'map_1',
                'draft': draft_obj.serialized
            }

            t1_data = {**match_data, 'is_team_1': True}
            t2_data = {**match_data, 'is_team_1': False}

            self.network.send_json_message(user=self.user_1, type='match_making', serialized_data=t1_data)
            self.network.send_json_message(user=self.user_2, type='match_making', serialized_data=t2_data)

            self.user_1 = None
            self.user_2 = None

    def create_draft(self) -> Draft:
        draft = self.server.draft_manager.create_draft(self.user_1, self.user_2)
        return draft