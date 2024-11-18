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

    def delete_team():
        pass

    def show_tournament_teams():
        db.show_data('tournament_team', 'tournament', 'team', 'id')

    def delete_tournament(name):
        id = db.get_data('id', 'tournament', name, 'name')
        db.delete_data('tournament', id)

    def list_of_tournaments():
        return db.show_table('tournament')