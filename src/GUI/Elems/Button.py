import pygame
from pygame import *

class Button:
    def __init__(self, screen, pos, text_input, font, base_color, hovering_color, draw_background=True):
        """
        Ініціалізація кнопки.

        :param screen: Екран для відображення.
        :param pos: Позиція центру кнопки (x, y).
        :param text_input: Текст кнопки.
        :param font: Об'єкт шрифту Pygame.
        :param base_color: Основний колір тексту.
        :param hovering_color: Колір тексту при наведенні.
        :param draw_background: Флаг для відображення напівпрозорого тла і контуру.
        """
        self.screen = screen
        self.x_pos, self.y_pos = pos
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.draw_background = draw_background
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.background_rect = self.text_rect.inflate(20, 10)

    def update(self):
        """Малює кнопку на екрані."""
        if self.draw_background:
            # Напівпрозоре чорне тло
            s = pygame.Surface(self.background_rect.size, pygame.SRCALPHA)
            s.fill((0, 0, 0, 128))  # Чорне тло з прозорістю 50%
            self.screen.blit(s, self.background_rect)
            # Білий контур
            pygame.draw.rect(self.screen, (255, 255, 255), self.background_rect, 2)
        self.screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        """Перевірка, чи була кнопка натиснута."""
        return self.text_rect.collidepoint(position)

    def changeColor(self, position):
        """Змінює колір тексту при наведенні."""
        if self.text_rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
