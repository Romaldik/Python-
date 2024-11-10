from ..DataBase.db_utils import dbUtils
from .TeamMember import Player, Coach, Staff

class Team:
    def __init__(self, name, location, trining_prog, period_of_sponsorship):
        self.name = name
        self.location = location
        self.trining_prog = trining_prog
        self.period_of_sponsorship = period_of_sponsorship
        self.db = dbUtils

    def create_team(self,):
        trining_prog_id = self.db.get_data('id', 'trainingProgram', self.trining_prog)

        data = (self.name, self.location, trining_prog_id[0], self.period_of_sponsorship)
        self.db.add_data('team', data)
    
    def delete_team(self, name):
        team_id = self.db.get_data('id', 'team', name)

        self.db.delete_data('team', team_id)

    def add_player(self, name, nickname, age, role, team):
        player = Player(name, nickname, age, role, team)
        player.add_people()

    def add_coach(self):
        pass

    def add_staff(self):
        pass

    def add_sponsor(self):
        pass  

    def change_team_players(self):
        pass

    def change_team_coach(self):
        pass

    def change_team_staff(self):
        pass

    def change_team_sponsor(self):
        pass
    
    def __str__(self):
        return f"Команда {self.name} має {len(self.members)} членів і {len(self.sponsors)} спонсорів."
