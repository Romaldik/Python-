import pygame, sys

class Dropdown:
    def __init__(self, x, y, options):
        self.rect = pygame.Rect(x, y, 200, 30)
        self.options = options
        self.selected = options[0]
        self.show_dropdown = False

    def toggle_dropdown(self):
        self.show_dropdown = not self.show_dropdown

    def select_option(self, option):
        self.selected = option
        self.show_dropdown = False

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        font_surface = pygame.font.Font("assets/main_menu_font.otf", 32).render(self.selected, True, (0, 0, 0))
        screen.blit(font_surface, (self.rect.x + 5, self.rect.y + 5))
        
        if self.show_dropdown:
            for index, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + 30 * (index + 1), self.rect.width, 30)
                pygame.draw.rect(screen, (255, 255, 255), option_rect)
                option_surface = pygame.font.Font("assets/main_menu_font.otf", 32).render(option, True, (0, 0, 0))
                screen.blit(option_surface, (option_rect.x + 5, option_rect.y + 5))
                if option_rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        self.select_option(option)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.toggle_dropdown()
