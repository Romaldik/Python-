from src.mypackage.TeamMember import Player
from src.mypackage.Team import Team

def create_team():
    a = Team('Navi', 'Europe', '1day', '12 days')
    a.create_team()
    #a.delete_team('Navi')

def add_player():
    a = Team('Navi')
    a.add_player('Aleksi', '1', 21, 'ingameleader')


if __name__ == "__main__":
    create_team()
    add_player()