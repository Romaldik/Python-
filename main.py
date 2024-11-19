
from src.mypackage.Team import Team
from src.mypackage.Sponsor import Sponsor 
from src.mypackage.Tournament import Tournament
from src.mypackage.TeamMember import Player, Coach, Staff
from src.mypackage.TrainingProgram import TrainingProgram

from src.GUI.Screens.Screens import ScreenManager, MainMenu, TeamsMenu, TournamentsMenu
import pygame

# Ініціалізація графічного інтерфесу
pygame.init()
pygame.display.set_caption("Кіберспортивний менеджер")
screen = pygame.display.set_mode((1920, 1080))
screen_manager = ScreenManager(screen)

""" def add_tournament_team():
    Tournament.add_team('Major', 'Navi')

def delete_tournament_team():
    Tournament.delete_team('Major', 'Navi') """

if __name__ == "__main__":
    """ #add_tournament_team()
    delete_tournament_team() """
    screen_manager.run()
