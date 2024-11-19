from src.mypackage.Team import Team
from src.mypackage.Sponsor import Sponsor 
from src.mypackage.Tournament import Tournament
from src.mypackage.TeamMember import Player, Coach, Staff
from src.mypackage.TrainingProgram import TrainingProgram

def create_training_program():
    TrainingProgram('Test', '365 days').create_training_program()
    print(TrainingProgram.list_of_training_programs())

def create_team():
    Team('Navi', 'Europe', '300 days').create_team()
    print(Team.list_of_teams())

def create_players():
    Player('Ivan', 'IM', 21, 'ingameleader').add_people()
    Coach('Andrei', 'Blaide', 21).add_people()
    Staff('Oleksandr', 20, 'caption').add_people()
    print(Player.list_of_players())
    print(Coach.list_of_players())
    print(Staff.list_of_players())

def create_sponsor():
    Sponsor('FavBet').create_sponsor()
    print(Sponsor.list_of_sponsors())

def create_tournament():
    Tournament('Major', '91 days', 'Europe', 1000000).create_tournament()
    print(Tournament.list_of_tournaments())

def add_people():
    Team.add_player('IM', 'Navi')
    Team.add_coach('Blaide', 'Navi')
    Team.add_staff('Oleksandr', 'Navi')
    print(Player.list_of_players())
    print(Coach.list_of_players())
    print(Staff.list_of_players())

def delete_team():
    Team.delete_team('Navi')
    print(Team.list_of_teams())

def delete_people():
    Player.delete_people('IM')
    Coach.delete_people('Blaide')
    Staff.delete_people('Oleksandr')
    print(Player.list_of_players())
    print(Coach.list_of_players())
    print(Staff.list_of_players())

def delete_train():
    TrainingProgram.delete_training_program('Test')
    print(TrainingProgram.list_of_training_programs())

def delete_sponsor():
    Sponsor.delete_sponsor('FavBet')
    print(Sponsor.list_of_sponsors())

def delete_tournament():
    Tournament.delete_tournament('Major')
    print(Tournament.list_of_tournaments())

def add_tournament_team():
    Tournament.add_team('Major', 'Navi')

def delete_tournament_team():
    Tournament.delete_team('Major', 'Navi')

def show_tournament_team():
    print(Tournament.show_tournament_teams('Major'))

def add_tournament_sponsor():
    Tournament.add_sponsor('Major', 'FavBet')

def delete_tournament_sponsor():
    Tournament.delete_sponsor('Major', 'FavBet')

def show_tournament_sponsor():
    print(Tournament.show_sponsors('Major'))

def add_team_sponsor():
    Team.add_sponsor('Navi', 'FavBet')

def delete_team_sponsor():
    Team.delete_sponsor('Navi', 'FavBet')

def show_team_sponsor():
    print(Team.show_sponsors('Navi'))

if __name__ == "__main__":
    #create_training_program()
    #create_team()
    #create_players()
    #add_people()
    #delete_team()
    #delete_people()
    #delete_train()
    #create_sponsor()
    #delete_sponsor()
    #create_tournament()
    #delete_tournament()
    #add_tournament_team()
    #delete_tournament_team()
    #show_tournament_team()
    #delete_tournament_sponsor()
    #show_tournament_sponsor()
    delete_team_sponsor()
    show_team_sponsor()