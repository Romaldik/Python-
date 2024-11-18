import pygame, sys

class InputBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.txt_surface = pygame.font.Font("assets/main_menu_font.otf", 32).render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Перевірка того, що користувач здійснив натиск на кнопку миші, коли курсор знаходиться на полі введення
            if self.rect.collidepoint(event.pos):
                self.active = not self.active  # Перемикаємо активність стану
            else:
                self.active = False
            self.color = pygame.Color('lightskyblue3') if self.active else pygame.Color('lightskyblue1')

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)  # Обробка уведення
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]  # Видалити останній символ
                else:
                    self.text += event.unicode  # Додати уведенний символ

        self.txt_surface = pygame.font.Font("assets/main_menu_font.otf", 32).render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)
