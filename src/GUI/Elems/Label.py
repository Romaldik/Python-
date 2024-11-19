import pygame
from pygame import *

class Label:
    def __init__(self, screen, text, pos, font, color=(255, 255, 255)):
        """
        Ініціалізація статичного тексту.

        :param screen: Екран для відображення тексту.
        :param text: Текст для відображення.
        :param pos: Позиція тексту (x, y).
        :param font: Об'єкт шрифту Pygame.
        :param color: Колір тексту.
        """
        self.screen = screen
        self.text = text
        self.x, self.y = pos
        self.font = font
        self.color = color
        self.rendered_text = self.font.render(self.text, True, self.color)
        self.rect = self.rendered_text.get_rect(topleft=(self.x, self.y))

    def update(self):
        """Відображає текст на екрані."""
        self.screen.blit(self.rendered_text, self.rect)

    def set_text(self, new_text):
        """Оновлює текст."""
        self.text = new_text
        self.rendered_text = self.font.render(self.text, True, self.color)
