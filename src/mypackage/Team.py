from ..DataBase.db_utils import dbUtils as db
from .TeamMember import Player, Coach, Staff
from .Sponsor import Sponsor

def get_team_id(name):
    result = db.get_data('id', 'team', name, 'name')
    return result
class Team:
    def __init__(self, name, location, period_of_sponsorship):
        self.name = name
        self.location = location
        self.period_of_sponsorship = period_of_sponsorship

    def create_team(self):
        data = (self.name, self.location, None, self.period_of_sponsorship)
        db.add_data('team', data)
    
    @staticmethod
    def delete_team(team):
        db.delete_data('team', (get_team_id(team),))

    def add_player(nickname, team):
        player_id = db.get_data('id', 'player', nickname, 'nickname')
        db.update_data('player', 'team_id', get_team_id(team), 'id', player_id[0])

    def add_coach(nickname, team):
        coach_id = db.get_data('id', 'coach', nickname, 'nickname')
        db.update_data('coach', 'team_id', get_team_id(team), 'id', coach_id[0])

    def add_staff(name, team):
        staff_id = db.get_data('id', 'staff', name, 'name')
        db.update_data('staff', 'team_id', get_team_id(team), 'id', staff_id[0])

    def add_training_program(program_name, team):
        program_id = db.get_data('id', 'trainingprogram', program_name, 'name')
        db.update_data('team', 'training_program_id', get_team_id(team), 'id', program_id[0])

    def add_sponsor(team, sponsor):
        team_id = db.get_data('id', 'team', team, 'name')
        sponsor_id = db.get_data('id', 'sponsor', sponsor, 'name')
        db.add_data('team_sponsor', (sponsor_id, team_id))

    def change_team_player(old_nickname, new_nickname, team):
        player_id = db.get_data('id', 'player', old_nickname, 'nickname')
        db.update_data('player', 'team_id', 'NULL', 'id', player_id[0])
        player_id = db.get_data('id', 'player', new_nickname, 'nickname')
        db.update_data('player', 'team_id', get_team_id(team), 'id', player_id[0])

    def change_team_coach(old_nickname, new_nickname, team):
        coach_id = db.get_data('id', 'coach', old_nickname, 'nickname')
        db.update_data('coach', 'team_id', 'NULL', 'id', coach_id[0])
        coach_id = db.get_data('id', 'coach', new_nickname, 'nickname')
        db.update_data('coach', 'team_id', get_team_id(team), 'id', coach_id[0])

    def change_team_staff(old_name, new_name, team):
        staff_id = db.get_data('id', 'staff', old_name, 'name')
        db.update_data('staff', 'team_id', 'NULL', 'id', staff_id[0])
        staff_id = db.get_data('id', 'staff', new_name, 'name')
        db.update_data('staff', 'team_id', get_team_id(team), 'id', staff_id[0])

    def delete_sponsor(team, sponsor):
        sponsor_id = db.get_data('id', 'sponsor', sponsor, 'name')[0]
        db.delete_data('team_sponsor', ['sponsor_id', get_team_id(team), 'team_id', sponsor_id])

    def show_sponsors(team):
        return db.show_exception_tables('team_sponsor', 'sponsor', ['sponsor_id', 'team_id'], get_team_id(team))
    
    def show_team_players(team):
        return db.show_team_member(get_team_id(team), "player")
    
    def show_team_coach(team):
        return db.show_team_member(get_team_id(team), "coach")
    
    def show_team_staff(team):
        return db.show_team_member(get_team_id(team), "staff")

    def list_of_teams():
        return db.show_data('Training_Program_Name', 'team', 'trainingprogram', 'training_program_id')