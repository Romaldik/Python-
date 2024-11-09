from abc import ABC, abstractmethod
from ..DataBase.db_utils import dbUtils

class TeamMember(ABC):
    def __init__(self, name:str, age:int, team:str):
        self.name = name
        self.age = age
        self.team = team
        self.db = dbUtils
    
    @abstractmethod  
    def add_people(self):
        pass

    @abstractmethod  
    def delete_people(self):
        pass
        
    def __str__(self):
        pass
    
class Player(TeamMember):
    def __init__(self, name, nickname, age, role, team):
        super().__init__(name, age, team)
        self.nickname = nickname
        self.role = role
    
    def add_people(self,):
        team_id = self.db.get_data('id', 'team', self.team)

        data = (self.name, self.nickname, self.age, self.role, team_id[0])
        self.db.add_data('player', data)

    def delete_people(self):
        player_id = self.db.get_data('id', 'player', self.name)

        self.db.delete_data('player', player_id)
    
    def __str__(self):
        return self.db.get_data('*', 'player', self.name)
    
class Coach(TeamMember):
    def __init__(self, name, nickname, age, team):
        super.__init__(name, age, team)
        self.nickname = nickname
        
    def add_people(self,):
        team_id = self.db.get_data('id', 'team', self.team)

        data = (self.name, self.nickname, self.age, team_id[0])
        self.db.add_data('coach', data)

    def delete_people(self):
        coach_id = self.db.get_data('id', 'coach', self.name)

        self.db.delete_data('coach', coach_id)

    def __str__(self):
        return self.db.get_data('*', 'coach', self.name)

class Staff(TeamMember):
    def __init__(self, name, age, role, team):
        super().__init__(name, age, team)
        self.role = role
    
    def add_people(self,):
        team_id = self.db.get_data('id', 'team', self.team)

        data = (self.name, self.age, self.role, team_id[0])
        self.db.add_data('staff', data)

    def delete_people(self):
        staff_id = self.db.get_data('id', 'staff', self.name)

        self.db.delete_data('staff', staff_id)

    def __str__(self):
        return self.db.get_data('*', 'staff', self.name)