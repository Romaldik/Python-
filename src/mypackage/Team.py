from ..DataBase.db_utils import dbUtils
from .TeamMember import Player, Coach, Staff

class Team:
    def __init__(self):
        self.db = dbUtils

    def create_team(self, name, location, trining_prog, period_of_sponsorship):
        trining_prog_id = self.db.get_data('id', 'trainingProgram', trining_prog)

        data = (name, location, trining_prog_id[0], period_of_sponsorship)
        self.db.add_data('team', data)
    
    def delete_team(self, name):
        team_id = self.db.get_data('id', 'team', name)

        self.db.delete_data('team', team_id)

    def change_team_player(self):
        pass

    def change_team_coach(self):
        pass

    def change_team_staff(self):
        pass

    def add_player(self):
        pass

    def add_coach(self):
        pass

    def add_staff(self):
        pass

    def add_sponsor(self):
        pass  
    
    def __str__(self):
        return f"Команда {self.name} має {len(self.members)} членів і {len(self.sponsors)} спонсорів."
