from ..DataBase.db_utils import dbUtils as db

class Tournament:
    def __init__(self, name, duration, location, prize_money):
        self.name = name
        self.duration = duration
        self.location = location
        self.prize_money = prize_money
    
    def create_tournament(self):
        data = (self.name, self.duration, self.location, self.prize_money)
        db.add_data('tournament', data)

    @staticmethod
    def add_team(tournament, team):
        tournament_id = db.get_data('id', 'tournament', tournament, 'name')
        team_id = db.get_data('id', 'team', team, 'name')
        db.add_data('tournament_team', (tournament_id, team_id))

    def delete_team(tournament, team):
        tournament_id = db.get_data('id', 'tournament', tournament, 'name')[0]
        team_id = db.get_data('id', 'team', team, 'name')[0]
        db.delete_data('tournament_team', ['tournament_id', tournament_id, 'team_id', team_id])

    def show_tournament_teams(tournament):
        tournament_id = db.get_data('id', 'tournament', tournament, 'name')[0]
        return db.show_exception_tables('tournament_team', 'team', ['tournament_id', 'team_id'], tournament_id)
    
    def add_sponsor(tournament, sponsor):
        tournament_id = db.get_data('id', 'tournament', tournament, 'name')
        sponsor_id = db.get_data('id', 'sponsor', sponsor, 'name')
        db.add_data('tournament_sponsor', (tournament_id, sponsor_id))

    def delete_sponsor(tournament, sponsor):
        tournament_id = db.get_data('id', 'tournament', tournament, 'name')[0]
        sponsor_id = db.get_data('id', 'sponsor', sponsor, 'name')[0]
        db.delete_data('tournament_sponsor', ['tournament_id', tournament_id, 'sponsor_id', sponsor_id])

    def show_sponsors(tournament):
        tournament_id = db.get_data('id', 'tournament', tournament, 'name')[0]
        return db.show_exception_tables('tournament_sponsor', 'sponsor', ['tournament_id', 'sponsor_id'], tournament_id)

    def delete_tournament(name):
        id = db.get_data('id', 'tournament', name, 'name')
        db.delete_data('tournament', id)

    def list_of_tournaments():
        return db.show_table('tournament')