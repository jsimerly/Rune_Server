from user import User
from uuid import uuid4
from typing import Literal
from dataclasses import dataclass, asdict
from copy import deepcopy
from enum import Enum, auto

@dataclass
class DraftCharacter:
    display_name: str
    char_id: int

    role: Literal['tank', 'damage', 'support']
    damage: int
    durability: int
    utility: int
    difficulty: int

    banned: bool = False
    picked: bool = False

    @property
    def serialized(self):
        return {
            'id': self.char_id,
            'display_name': self.display_name,
            'role': self.role,
            'damage': self.damage,
            'durability': self.durability,
            'utility': self.utility,
            'difficulty': self.difficulty,
        }
    
characters: dict[int, DraftCharacter] = {
    1: DraftCharacter('Athlea', 1,
        role= 'damage',
        damage=0,
        durability=0,
        utility=0,
        difficulty=0,
    ),
    2: DraftCharacter('Bizi', 2, 
        role= 'damage',
        damage=0,
        durability=0,
        utility=0,
        difficulty=0,
    ),
    3: DraftCharacter('Bolinda', 3, 
        role= 'damage',
        damage=0,
        durability=0,
        utility=0,
        difficulty=0,
    ),
    4: DraftCharacter('Crud', 4, 
        role= 'damage',
        damage=0,
        durability=0,
        utility=0,
        difficulty=0,
    ),
    5: DraftCharacter('Emily', 5, 
        role= 'damage',
        damage=0,
        durability=0,
        utility=0,
        difficulty=0,
    ),
    6: DraftCharacter('Herc', 6, 
        role= 'damage',
        damage=0,
        durability=0,
        utility=0,
        difficulty=0,
    ),
    7: DraftCharacter('Ivan', 7, 
        role= 'damage',
        damage=0,
        durability=0,
        utility=0,
        difficulty=0,
    ),
    8: DraftCharacter('Judy', 8, 
        role= 'damage',
        damage=0,
        durability=0,
        utility=0,
        difficulty=0,
    ),
    9: DraftCharacter('Kane', 9, 
        role= 'damage',
        damage=0,
        durability=0,
        utility=0,
        difficulty=0,
    ),
    10: DraftCharacter('Lu', 10, 
        role= 'damage',
        damage=0,
        durability=0,
        utility=0,
        difficulty=0,
    ),
    11: DraftCharacter('Navi', 11, 
        role= 'damage',
        damage=0,
        durability=0,
        utility=0,
        difficulty=0,
    ),
    12: DraftCharacter('Papa', 12, 
        role= 'damage',
        damage=0,
        durability=0,
        utility=0,
        difficulty=0,
    ),
    13: DraftCharacter('Tim', 13, 
        role= 'damage',
        damage=0,
        durability=0,
        utility=0,
        difficulty=0,
    ),
}

@dataclass
class DraftTeam:
    def __init__(self, user: User) -> None:
        self.id = str(uuid4())
        self.user = user
        self.bans: list[DraftCharacter] = []
        self.picks: list[DraftCharacter] = []

    @property
    def serialized(self):
        return {
            'id': self.id,
            'user': self.user.serialized,
            'bans': [asdict(ban) for ban in self.bans],
            'picks': [asdict(pick) for pick in self.picks],
        }
    
class DraftPhases_1_3(Enum):
    TEAM_1_BAN = auto()
    TEAM_2_BAN = auto()
    TEAM_1_PICK_1 = auto()
    TEAM_2_PICK_1 = auto()
    TEAM_2_PICK_2 = auto()
    TEAM_1_PICK_2 = auto()
    TEAM_1_PICK_3 = auto()
    TEAM_2_PICK_3 = auto()

    @classmethod
    def next_phase(cls, current_phase):
        member = list(cls)
        index = member.index(current_phase)
        if index < len(member) - 1:
            return member[index + 1]
        else:
            return None

class Draft:
    def __init__(self, user_1: User, user_2: User) -> None:
        self.id = str(uuid4())
        self.team_1 = DraftTeam(user_1)
        self.team_2 = DraftTeam(user_2)
        self.available_picks = deepcopy(characters)
        self.unavailable: list[DraftCharacter] = []
        self.current_phase = DraftPhases_1_3.TEAM_1_BAN

    def next_phase(self):
        self.current_phase = DraftPhases_1_3.next_phase(self.current_phase)
        if self.current_phase is None:
            print("COMPLETE THE DRAFT")

    def ban_character(self, user: User, character_id: int):
        team = self.team_1 if self.team_1.user == user else self.team_2

        character = self.get_character_from_pool(character_id)
        character.banned = True
        team.bans.append(character)

    def pick_character(self, user: User, character_id: int):
        team = self.team_1 if self.team_1.user == user else self.team_2

        character = self.get_character_from_pool(character_id)
        character.picked = True
        team.picks.append(character)

    def get_character_from_pool(self, character_id: int) -> DraftCharacter:
        return self.available_picks.pop(character_id)
    
    @property
    def serialized(self):
        return {
            'id': self.id,
            'team_1': self.team_1.serialized,
            'team_2': self.team_2.serialized,
            'current_phase': self.current_phase.value,
            'character_info': {key: char.serialized for key, char in characters.items()},
            'available': [char.char_id for char in self.available_picks.values()],
            'unavailable': [char.char_id for char in self.unavailable]
        }


class DraftManager:
    bans = 1
    picks = 3

    def __init__(self, server) -> None:
        self.active_drafts: dict[int, Draft] = {}

    def create_draft(self, user_1: User, user_2: User) -> Draft:
        return Draft(user_1, user_2)
