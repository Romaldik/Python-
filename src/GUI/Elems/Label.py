class Label:
    def __init__(self, screen, text, pos, font, color=(255, 255, 255)):
        """
        Инициализация статичного текста.

        :param screen: Экран для отображения текста.
        :param text: Текст для отображения.
        :param pos: Позиция текста (x, y).
        :param font: Объект шрифта Pygame.
        :param color: Цвет текста.
        """
        self.screen = screen
        self.text = text
        self.x, self.y = pos
        self.font = font
        self.color = color
        self.rendered_text = self.font.render(self.text, True, self.color)
        self.rect = self.rendered_text.get_rect(topleft=(self.x, self.y))

    def update(self):
        """Отображает текст на экране."""
        self.screen.blit(self.rendered_text, self.rect)

    def set_text(self, new_text):
        """Обновляет текст."""
        self.text = new_text
        self.rendered_text = self.font.render(self.text, True, self.color)
