import pygame, sys
class InputBox:
    def __init__(self, screen, pos, size, font, text=''):
        self.screen = screen
        self.rect = pygame.Rect(pos, size)
        self.color = (0, 0, 0, 128)
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Проверяем, нажал ли пользователь на поле ввода
            if self.rect.collidepoint(event.pos):
                self.active = not self.active  # Переключение состояния активности
            else:
                self.active = False
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)  # Обработка текста
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]  # Удаляем последний символ
                else:
                    self.text += event.unicode  # Добавляем новый символ

                # Обновляем текстовую поверхность
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self):
        # Рисуем текст
        self.screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Рисуем рамку
        pygame.draw.rect(self.screen, self.color, self.rect, 2)
