from src.mypackage.Team import Team
from src.mypackage.Sponsor import Sponsor 
from src.mypackage.Tournament import Tournament
from src.mypackage.TeamMember import Player, Coach, Staff
from src.mypackage.TrainingProgram import TrainingProgram

def create_team():
    a = Team('Navi', 'Europe', '1day', '12 days')
    a.create_team()
    #a.delete_team('Navi')

def add_player():
    Team.add_player('IM', '1', 21, 'ingameleader', 'Navi')
    #Team.delete_team('Navi')


if __name__ == "__main__":
    #Team('MOUZ', 'Europe', '12 days').create_team()
    Team.delete_team('Navi')
    #create_team()
    #add_player()
    #Team.add_player_to_the_team('Aleksi', 'Navi')
    #Team.change_team_player('Aleksi', 'IM', 'Navi')
    #print(TrainingProgram.list_of_training_programs())
    #Team.add_training_program('Test', 'MOUZ')