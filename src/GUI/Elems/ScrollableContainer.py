import pygame


class ScrollableContainer:
    def __init__(self, screen, pos, size, bg_color=(0, 0, 0, 128), scroll_color="White", border_color="White"):
        """
        Инициализация прокручиваемого контейнера.

        :param screen: экран для отрисовки.
        :param pos: позиция контейнера (x, y).
        :param size: размер контейнера (width, height).
        :param bg_color: цвет фона контейнера (по умолчанию черный и полупрозрачный).
        :param scroll_color: цвет полосы прокрутки.
        :param border_color: цвет контура контейнера.
        """
        self.screen = screen
        self.x, self.y = pos
        self.width, self.height = size
        self.bg_color = bg_color
        self.scroll_color = scroll_color
        self.border_color = border_color

        self.elements = []  # Список элементов для отображения
        self.scroll_offset = 0  # Текущий сдвиг прокрутки
        self.scroll_speed = 10  # Скорость прокрутки

        # Прямоугольники области содержимого и прокрутки
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.scroll_bar_rect = pygame.Rect(
            self.x + self.width - 20, self.y, 20, self.height
        )

    def add_element(self, element):
        """
        Добавить элемент в контейнер.
        :param element: объект, который должен поддерживать метод draw(surface).
        """
        self.elements.append(element)

    def draw(self):
        """
        Отрисовка контейнера и его содержимого.
        """
        # Отрисовка фона и границы
        bg_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        bg_surface.fill(self.bg_color)
        self.screen.blit(bg_surface, (self.x, self.y))
        pygame.draw.rect(self.screen, self.border_color, self.rect, 2)

        # Отрисовка содержимого
        visible_area = pygame.Rect(self.x, self.y, self.width - 20, self.height)
        content_surface = pygame.Surface(
            (self.width - 20, max(self.height, len(self.elements) * 50)), pygame.SRCALPHA
        )
        content_surface.fill((0, 0, 0, 0))  # Прозрачный фон

        for i, element in enumerate(self.elements):
            element_y = i * 50 - self.scroll_offset
            if 0 <= element_y < self.height:  # Отображать только видимые элементы
                element.rect.y = element_y
                element.update()

        self.screen.blit(content_surface, (self.x, self.y), visible_area)

        # Отрисовка полосы прокрутки
        pygame.draw.rect(self.screen, self.scroll_color, self.scroll_bar_rect)

    def handle_event(self, event):
        """
        Обработка событий для прокрутки.
        :param event: событие pygame.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Прокрутка вверх
                self.scroll_offset = max(self.scroll_offset - self.scroll_speed, 0)
            elif event.button == 5:  # Прокрутка вниз
                max_offset = max(len(self.elements) * 50 - self.height, 0)
                self.scroll_offset = min(self.scroll_offset + self.scroll_speed, max_offset)

    def update(self):
        """
        Обновить и отобразить контейнер.
        """
        self.draw()
