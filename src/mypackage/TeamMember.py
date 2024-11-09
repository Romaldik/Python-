from abc import ABC, abstractmethod
from ..DataBase.db_utils import select_query, execute_query 

class TeamMember(ABC):
    def __init__(self, name:str, age:int, team:str):
        self.name = name
        self.age = age
        self.team = team
    
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
    
    def add_people(self):
        query = 'SELECT id FROM Team WHERE name = %s;'
        team_id = select_query(query, (self.team,))

        add_player = """
        INSERT INTO Player (name, nickname, age, role, team_id)
        VALUES (%s, %s, %s, %s, %s);
        """
        data = (self.name, self.nickname, self.age, self.role, team_id)
        execute_query(add_player, data)

    def delete_people(self):
        query = 'SELECT id FROM Player WHERE name = %s;'
        player_id = select_query(query, (self.name,))

        delete_query = "DELETE FROM Player WHERE id = %s"
        execute_query(delete_query, player_id)
    
    def __str__(self):
        return f"{self.name} ({self.role}), навички {self.skills}"
    
class Coach(TeamMember):
    def __init__(self, name, nickname, age, team):
        super.__init__(name, age, team)
        self.nickname = nickname
        
    def add_people(self):
        query = 'SELECT id FROM Team WHERE name = %s;'
        team_id = select_query(query, (self.team,))

        add_coach = """
        INSERT INTO Coach (name, nickname, age, team_id)
        VALUES (%s, %s, %s, %s);
        """
        data = (self.name, self.nickname, self.age, team_id)
        execute_query(add_coach, data)

    def delete_people(self):
        query = 'SELECT id FROM Coach WHERE name = %s;'
        coach_id = select_query(query, (self.name,))

        delete_query = "DELETE FROM Coach WHERE id = %s"
        execute_query(delete_query, coach_id)

class Staff(TeamMember):
    def __init__(self, name, age, role, team):
        super().__init__(name, age, team)
        self.role = role
    
    def add_people(self):
        query = 'SELECT id FROM Team WHERE name = %s;'
        team_id = select_query(query, (self.team,))

        add_staff = """
        INSERT INTO Staff (name, age, role, team_id)
        VALUES (%s, %s, %s, %s);
        """
        data = (self.name, self.age, self.role, team_id)
        execute_query(add_staff, data)

    def delete_people(self):
        query = 'SELECT id FROM Staff WHERE name = %s;'
        staff_id = select_query(query, (self.name,))

        delete_query = "DELETE FROM Staff WHERE id = %s"
        execute_query(delete_query, staff_id)