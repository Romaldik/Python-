from src.GUI.Screens import ScreenManager
import pygame

# Инициализация графического интерфейса
pygame.init()
pygame.display.set_caption("Кіберспортивний менеджер")
screen = pygame.display.set_mode((1920, 1080))
screen_manager = ScreenManager(screen)

if __name__ == "__main__":
    screen_manager.run()
