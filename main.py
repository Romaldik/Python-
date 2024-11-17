from src.mypackage.Team import Team
from src.mypackage.TeamMember import Player

def create_team():
    a = Team('Navi', 'Europe', '1day', '12 days')
    a.create_team()
    #a.delete_team('Navi')

def add_player():
    Team.add_player('IM', '1', 21, 'ingameleader', 'Navi')
    #Team.delete_team('Navi')


if __name__ == "__main__":
    #create_team()
    #add_player()
    #Team.add_player_to_the_team('Aleksi', 'Navi')
    #Team.change_team_player('Aleksi', 'IM', 'Navi')
    print(Player.list_of_players())