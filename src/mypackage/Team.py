from ..DataBase.db_utils import dbUtils as db
from .TeamMember import Player, Coach, Staff
from .Sponsor import Sponsor

def get_team_id(name):
    return db.get_data('id', 'team', name)[0]
class Team:
    def __init__(self, name, location, period_of_sponsorship):
        self.name = name
        self.location = location
        self.period_of_sponsorship = period_of_sponsorship

    def create_team(self,):
        data = (self.name, self.location, self.period_of_sponsorship)
        db.add_data('team', data)
    
    @staticmethod
    def delete_team(name):
        db.delete_data('team', get_team_id(name))

    def add_player(name, team):
        player_id = db.get_data('id', 'player', name)
        db.update_data('player', 'team_id', get_team_id(team), 'id', player_id[0])

    def add_coach(name, team):
        coach_id = db.get_data('id', 'coach', name)
        db.update_data('coach', 'team_id', get_team_id(team), 'id', coach_id[0])

    def add_staff(name, team):
        staff_id = db.get_data('id', 'staff', name)
        db.update_data('staff', 'team_id', get_team_id(team), 'id', staff_id[0])

    def add_training_program(program_name, team):
        program_id = db.get_data('id', 'trainingprogram', program_name)
        db.update_data('team', 'training_program_id', get_team_id(team), 'id', program_id[0])

    def add_sponsor(name, team):
        pass

    def change_team_player(old_name, new_name, team):
        player_id = db.get_data('id', 'player', old_name)
        db.update_data('player', 'team_id', 'NULL', 'id', player_id[0])
        player_id = db.get_data('id', 'player', new_name)
        db.update_data('player', 'team_id', get_team_id(team), 'id', player_id[0])

    def change_team_coach(old_name, new_name, team):
        coach_id = db.get_data('id', 'coach', old_name)
        db.update_data('coach', 'team_id', 'NULL', 'id', coach_id[0])
        coach_id = db.get_data('id', 'coach', new_name)
        db.update_data('coach', 'team_id', get_team_id(team), 'id', coach_id[0])

    def change_team_staff(old_name, new_name, team):
        staff_id = db.get_data('id', 'staff', old_name)
        db.update_data('staff', 'team_id', 'NULL', 'id', staff_id[0])
        staff_id = db.get_data('id', 'staff', new_name)
        db.update_data('staff', 'team_id', get_team_id(team), 'id', staff_id[0])

    def change_team_sponsor():
        pass

    def list_of_teams():
        return db.show_data('Training_Program_Name', 'team', 'trainingprogram', 'training_program_id')