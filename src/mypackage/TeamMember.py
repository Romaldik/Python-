from abc import ABC, abstractmethod
from ..DataBase.db_utils import dbUtils as db

class TeamMember(ABC):
    def __init__(self, name:str, age:int, team:str):
        self.name = name
        self.age = age
        #self.team = team
    
    @abstractmethod  
    def add_people(self):
        pass

    @abstractmethod  
    def delete_people(self):
        pass

    def list_of_players():
        pass
        
class Player(TeamMember):
    def __init__(self, name, nickname, age, role, team):
        super().__init__(name, age, team)
        self.nickname = nickname
        self.role = role
    
    def add_people(self,):
        data = (self.name, self.nickname, self.age, self.role)
        db.add_data('player', data)

    @staticmethod
    def delete_people(name):
        player_id = db.get_data('id', 'player', name)
        db.delete_data('player', player_id)

    def list_of_players():
        return db.show_data('Team_Name', 'player', 'team', 'team_id')
    
class Coach(TeamMember):
    def __init__(self, name, nickname, age, team):
        super.__init__(name, age, team)
        self.nickname = nickname
        
    def add_people(self,):
        data = (self.name, self.nickname, self.age)
        db.add_data('coach', data)
    
    @staticmethod
    def delete_people(name):
        coach_id = db.get_data('id', 'coach', name)
        db.delete_data('coach', coach_id)

    def list_of_coachs():
        return db.show_data('Team_Name', 'coach', 'team', 'team_id')

class Staff(TeamMember):
    def __init__(self, name, age, role, team):
        super().__init__(name, age, team)
        self.role = role
    
    def add_people(self,):
        data = (self.name, self.age, self.role)
        db.add_data('staff', data)
    
    @staticmethod
    def delete_people(name):
        staff_id = db.get_data('id', 'staff', name)
        db.delete_data('staff', staff_id)

    def list_of_staffs():
        return db.show_data('Team_Name', 'staff', 'team', 'team_id')