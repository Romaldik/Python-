import pygame


class ToggleBox:
    def __init__(self, screen, pos, size, text, font):
        """
        Инициализация ToggleBox.

        :param screen: экран для отрисовки.
        :param pos: позиция ToggleBox (x, y).
        :param size: размер ToggleBox (width, height).
        :param text: текст на ToggleBox.
        :param font: шрифт для текста.
        """
        self.screen = screen
        self.x, self.y = pos
        self.width, self.height = size
        self.text = text
        self.font = font

        # Цвета по умолчанию
        self.base_color = (0, 0, 0, 128)  # Прозрачно-чёрный
        self.hovering_color = (0, 0, 0, 255)  # Полностью чёрный
        self.toggled_color = (139, 0, 0)  # Тёмно-бордовый

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text_surface = self.font.render(self.text, True, "White")
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

        self.is_toggled = False

    def draw(self):
        """
        Отрисовка ToggleBox.
        """
        # Определение цвета в зависимости от состояния
        if self.is_toggled:
            color = self.toggled_color
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            color = self.hovering_color
        else:
            color = self.base_color

        # Отрисовка фона и текста
        pygame.draw.rect(self.screen, color, self.rect)
        pygame.draw.rect(self.screen, "White", self.rect, 2)  # Белая рамка
        self.screen.blit(self.text_surface, self.text_rect)

    def handle_event(self, event):
        """
        Обработка событий для ToggleBox.
        :param event: событие pygame.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # ЛКМ
            if self.rect.collidepoint(event.pos):
                self.is_toggled = not self.is_toggled  # Переключить состояние
                return True
        return False

    def is_selected(self):
        """
        Проверка, находится ли ToggleBox в состоянии "выбран".
        :return: True, если выбран, иначе False.
        """
        return self.is_toggled

    def reset(self):
        """
        Сброс состояния ToggleBox.
        """
        self.is_toggled = False
