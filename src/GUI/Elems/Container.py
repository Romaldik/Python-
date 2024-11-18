import pygame

class Container:
    def __init__(self, screen, pos, size, background_color=(0, 0, 0), alpha=150, border_color=None, border_thickness=0):
        """
        Инициализация контейнера.

        :param screen: Экран, на котором будет отображаться контейнер.
        :param pos: Позиция контейнера (x, y).
        :param size: Размер контейнера (ширина, высота).
        :param background_color: Цвет фона контейнера (по умолчанию чёрный).
        :param alpha: Прозрачность фона (от 0 до 255).
        :param border_color: Цвет границы (None для отсутствия границы).
        :param border_thickness: Толщина границы (0 для отсутствия границы).
        """
        self.screen = screen
        self.x, self.y = pos
        self.width, self.height = size
        self.background_color = background_color
        self.alpha = alpha
        self.border_color = border_color
        self.border_thickness = border_thickness

        # Создаём поверхность для контейнера
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.fill((*self.background_color, self.alpha))

    def update(self):
        """Отображает контейнер на экране."""
        # Отрисовка полупрозрачного фона
        self.screen.blit(self.surface, (self.x, self.y))

        # Если указана граница, отрисовываем её
        if self.border_color and self.border_thickness > 0:
            pygame.draw.rect(
                self.screen,
                self.border_color,
                (self.x, self.y, self.width, self.height),
                self.border_thickness,
            )
