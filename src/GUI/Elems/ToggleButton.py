class ToggleButton():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, active_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.active_color = active_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.is_active = False  # Состояние переключателя

    def update(self, screen):
        # Изменяем цвет в зависимости от состояния
        if self.is_active:
            self.text = self.font.render(self.text_input, True, self.active_color)
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.is_active = not self.is_active  # Переключение состояния
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            if not self.is_active:  # Меняем цвет только если кнопка не активна
                self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            if not self.is_active:  # Если кнопка не активна, возвращаем базовый цвет
                self.text = self.font.render(self.text_input, True, self.base_color)
