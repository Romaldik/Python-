from ..Screens.__init__ import pygame, sys, Button, ToggleButton, InputBox, Dropdown, Container, ScrollableContainer, Label, ToggleBox
from src.DataBase.db_utils import dbUtils as db
from abc import ABC, abstractmethod
from src.mypackage import *


# Основной класс экрана
class ScreenManager:
    def __init__(self, screen):
        self.screen = screen
        self.screens = {
            "main_menu": MainMenu(self.screen, self),
            "teams_menu": TeamsMenu(self.screen, self),
            "tournaments_menu": TournamentsMenu(self.screen, self)
        }
        self.current_screen = self.screens["main_menu"]

    def switch_to(self, name):
        self.current_screen = self.screens[name]

    def run(self):
        while self.current_screen:
            self.current_screen.update()


# Головне меню програми
class MainMenu:
    def __init__(self, screen, manager):
        self.SCREEN = screen
        self.manager = manager  # Диспетчер экранов
        self.MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Загрузка фона и текста
        self.BG = pygame.image.load("assets/Background.png")
        self.MENU_TEXT = get_font(100).render("ГОЛОВНЕ МЕНЮ", True, "#b68f40")
        self.MENU_RECT = self.MENU_TEXT.get_rect(center=(self.SCREEN.get_width() // 2, 150))

        # Центрирование кнопок
        button_width, button_height = 400, 100
        button_spacing = 50
        center_x = self.SCREEN.get_width() // 2
        start_y = 350

        # Инициализация кнопок
        self.TEAMS_BUTTON = Button(
            image=None, 
            pos=(center_x, start_y), 
            text_input="Команди", 
            font=get_font(75), 
            base_color="#d7fcd4", 
            hovering_color="White"
        )
        self.TOURNAMENTS_BUTTON = Button(
            image=None, 
            pos=(center_x, start_y + button_height + button_spacing), 
            text_input="Турніри", 
            font=get_font(75), 
            base_color="#d7fcd4", 
            hovering_color="White"
        )
        self.QUIT_BUTTON = Button(
            image=None, 
            pos=(center_x, start_y + 2 * (button_height + button_spacing)), 
            text_input="Вихід", 
            font=get_font(75), 
            base_color="#d7fcd4", 
            hovering_color="White"
        )

    def update(self):
        fade_effect(self.SCREEN, duration=300, fade_in=True)
        while True:
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            # Отрисовка фона и элементов меню
            self.SCREEN.blit(self.BG, (0, 0))
            self.SCREEN.blit(self.MENU_TEXT, self.MENU_RECT)
            for button in [self.TEAMS_BUTTON, self.TOURNAMENTS_BUTTON, self.QUIT_BUTTON]:
                button.changeColor(self.MENU_MOUSE_POS)
                button.update(self.SCREEN)

            # Обработка событий (переходы между меню)
            if self.event_handler():
                break

            pygame.display.update()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.TEAMS_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    self.manager.switch_to("teams_menu")  # Переключение на экран команд
                    return True
                if self.TOURNAMENTS_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    self.manager.switch_to("tournaments_menu")  # Переключение на экран турниров
                    return True
                if self.QUIT_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        return False



# Меню команд
class TeamsMenu:
    def __init__(self, screen, manager):
        self.SCREEN = screen
        self.manager = manager
        self.MENU_MOUSE_POS = pygame.mouse.get_pos()

        self.BG = pygame.image.load("assets/TeamsBackground.png")
        self.TITLE_TEXT = get_font(75).render("Команди", True, "White")
        self.TITLE_RECT = self.TITLE_TEXT.get_rect(topleft=(20, 20))

        # Ліва частина вікна: Список команд
        self.teams = Team.list_of_teams()  # Отримання списку команд з бази даних
        if self.teams == None:
            self.teams = []
        else:
            self.toggle_boxes = [
                ToggleBox(
                    self.SCREEN,
                    (20, 120 + i * 60),
                    (300, 40),
                    team["Training_Program_Name"],
                    get_font(30),
                    base_color=(0, 0, 0, 128),
                    hovering_color="White",
                    toggled_color="Green",
                )
                for i, team in enumerate(self.teams)
            ]

        self.selected_team = None

        # Центральная часть: прокручиваемый контейнер
        self.scrollable_container = ScrollableContainer(self.SCREEN, (350, 120), (700, 600))

        # Правая часть: кнопки действий
        self.ADD_MEMBER_BUTTON = Button(image=None, pos=(1300, 200), text_input="Додати члена", font=get_font(30),
                                        base_color="White", hovering_color="Green")
        self.REMOVE_MEMBER_BUTTON = Button(image=None, pos=(1300, 300), text_input="Видалити члена", font=get_font(30),
                                           base_color="White", hovering_color="Green")
        self.VIEW_INFO_BUTTON = Button(image=None, pos=(1300, 400), text_input="Переглянути дані", font=get_font(30),
                                       base_color="White", hovering_color="Green")

        # Нижняя часть: кнопки сохранения, отмены и возврата
        self.SAVE_BUTTON = Button(image=None, pos=(800, 750), text_input="Зберегти", font=get_font(30),
                                  base_color="White", hovering_color="Green")
        self.CANCEL_BUTTON = Button(image=None, pos=(1000, 750), text_input="Скасувати", font=get_font(30),
                                    base_color="White", hovering_color="Green")
        self.GO_BACK_BUTTON = Button(image=None, pos=(1200, 750), text_input="Повернутися", font=get_font(30),
                                     base_color="White", hovering_color="Green")

    def display_team_members(self):
        """Обновити центральний контейнер для відображення членів вибраної команди."""
        self.scrollable_container.elements = []
        if self.selected_team:
            team_id = self.selected_team["id"]
            members = db.show_data("name, age, role", "player", "team", team_id)
            for member in members:
                label = Label(self.SCREEN, f"{member['name']} ({member['role']})", pos=(350, 120), font=get_font(25), color="White")
                self.scrollable_container.add_element(label)

    def event_handler(self):
        """Обробка подій."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Прокрутка контейнера
            self.scrollable_container.handle_event(event)

            # Логіка для вибору команди
            for toggle_box, team in zip(self.toggle_boxes, self.teams):
                toggle_box.handle_event(event)
                if toggle_box.is_selected:
                    self.selected_team = team
                    self.display_team_members()

            # Кнопки
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.GO_BACK_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    self.manager.switch_to("main_menu")
                    return True
                if self.ADD_MEMBER_BUTTON.checkForInput(self.MENU_MOUSE_POS) and self.selected_team:
                    self.add_member()
                if self.REMOVE_MEMBER_BUTTON.checkForInput(self.MENU_MOUSE_POS) and self.selected_team:
                    self.remove_member()
                if self.VIEW_INFO_BUTTON.checkForInput(self.MENU_MOUSE_POS) and self.selected_team:
                    self.view_team_info()

        return False

    def add_member(self):
        """Додати учасника до вибраної команди."""
        if not self.selected_team:
            return
        # Логіка додавання нового учасника через Team.add_player або схожі методи

    def remove_member(self):
        """Видалити учасника з вибраної команди."""
        if not self.selected_team:
            return
        # Логіка видалення учасника

    def view_team_info(self):
        """Переглянути інформацію про команду."""
        if not self.selected_team:
            return
        print(Team(self.selected_team["Training_Program_Name"]))

    def update(self):
        """Основний цикл оновлення екрану."""
        fade_effect(self.SCREEN, duration=300, fade_in=True)
        while True:
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            # Отрисовка фона и элементов
            self.SCREEN.blit(self.BG, (0, 0))
            self.SCREEN.blit(self.TITLE_TEXT, self.TITLE_RECT)

            # Відображення списку команд
            for toggle_box in self.toggle_boxes:
                toggle_box.draw()

            # Центральний контейнер
            self.scrollable_container.update()

            # Кнопки
            for button in [self.ADD_MEMBER_BUTTON, self.REMOVE_MEMBER_BUTTON, self.VIEW_INFO_BUTTON,
                           self.SAVE_BUTTON, self.CANCEL_BUTTON, self.GO_BACK_BUTTON]:
                button.changeColor(self.MENU_MOUSE_POS)
                button.update(self.SCREEN)

            # Обробка подій
            if self.event_handler():
                break

            pygame.display.update()




# Меню турнірів
class TournamentsMenu:
    def __init__(self, screen, manager):
        self.SCREEN = screen
        self.manager = manager
        self.MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Загрузка фона и заголовка
        self.BG = pygame.image.load("assets/TournamentsBackground.png")
        self.TITLE_TEXT = get_font(75).render("Турніри", True, "White")
        self.TITLE_RECT = self.TITLE_TEXT.get_rect(topleft=(20, 20))

        # Инициализация кнопок
        self.ADD_TOURNAMENT_BUTTON = Button(image=None, pos=(1400, 200), text_input="Додати турнір", font=get_font(50), base_color="White", hovering_color="Green")
        self.DELETE_TOURNAMENT_BUTTON = Button(image=None, pos=(1400, 300), text_input="Видалити турнір", font=get_font(50), base_color="White", hovering_color="Green")
        self.GO_BACK_BUTTON = Button(image=None, pos=(1100, 950), text_input="Повернутися", font=get_font(50), base_color="White", hovering_color="Green")

        # Пример данных для списка турниров
        self.tournaments_list = [
            {"name": "Турнір 1", "location": "Київ", "prize_fund": "5000", "status": "Скоро почнеться", "start_date": "2024-12-01", "end_date": "2024-12-05"},
            {"name": "Турнір 2", "location": "Львів", "prize_fund": "10000", "status": "Триває", "start_date": "2024-11-20", "end_date": "2024-11-25"},
        ]

    def update(self):
        fade_effect(self.SCREEN, duration=300, fade_in=True)
        while True:
            self.MENU_MOUSE_POS = pygame.mouse.get_pos()

            # Отрисовка фона и заголовка
            self.SCREEN.blit(self.BG, (0, 0))
            self.SCREEN.blit(self.TITLE_TEXT, self.TITLE_RECT)

            # Отрисовка кнопок
            for button in [self.ADD_TOURNAMENT_BUTTON, self.DELETE_TOURNAMENT_BUTTON, self.GO_BACK_BUTTON]:
                button.changeColor(self.MENU_MOUSE_POS)
                button.update(self.SCREEN)

            # Отрисовка списка турниров
            for i, tournament in enumerate(self.tournaments_list):
                TOURNAMENT_TEXT = get_font(50).render(
                    f"{tournament['name']}, {tournament['location']}, Призовий фонд: {tournament['prize_fund']}, Статус: {tournament['status']}, "
                    f"Початок: {tournament['start_date']}, Кінець: {tournament['end_date']}",
                    True,
                    "White",
                )
                TOURNAMENT_RECT = TOURNAMENT_TEXT.get_rect(topleft=(20, 100 + i * 60))
                self.SCREEN.blit(TOURNAMENT_TEXT, TOURNAMENT_RECT)

                # Подсветка при наведении
                if TOURNAMENT_RECT.collidepoint(self.MENU_MOUSE_POS):
                    pygame.draw.rect(self.SCREEN, (100, 100, 100), TOURNAMENT_RECT)

            # Обработка событий
            if self.event_handler():
                break

            pygame.display.update()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.ADD_TOURNAMENT_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    # Логика добавления турнира
                    pass
                if self.DELETE_TOURNAMENT_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    # Логика удаления турнира
                    pass
                if self.GO_BACK_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    self.manager.switch_to("main_menu")  # Возврат к главному меню
                    return True

        return False


# Абстрактний клас вспливаючого меню
class PopupMenu(ABC):
    def __init__(self, screen, background_color=(0, 0, 0), alpha=150):
        self.screen = screen
        self.background_color = background_color  # Цвет затемнения фона
        self.alpha = alpha  # Прозрачность затемнения
        self.rect_color = (255, 255, 255)  # Цвет прямоугольника (белый контур)
        self.rect_thickness = 5  # Толщина контура
        self.is_visible = False  # Показывать или скрывать меню
        self.menu_width, self.menu_height = 600, 400
        self.x_pos = (screen.get_width() - self.menu_width) // 2
        self.y_pos = (screen.get_height() - self.menu_height) // 2
        self.menu_rect = pygame.Rect(self.x_pos, self.y_pos, self.menu_width, self.menu_height)
        
        # Кнопка "повернутися"
        self.return_button = Button(
            image=None,
            pos=(self.x_pos + self.menu_width // 2, self.y_pos + self.menu_height - 50),
            text_input="Повернутися",
            font=pygame.font.Font(None, 40),
            base_color="White",
            hovering_color="Yellow"
        )

    def show(self):
        """Показать всплывающее меню."""
        self.is_visible = True

    def hide(self):
        """Скрыть всплывающее меню."""
        self.is_visible = False

    def update(self):
        """Обновление и отображение всплывающего меню."""
        if not self.is_visible:
            return
        
        # Затемнение заднего фона
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((*self.background_color, self.alpha))
        self.screen.blit(overlay, (0, 0))

        # Отрисовка прямоугольника с контуром
        pygame.draw.rect(self.screen, self.rect_color, self.menu_rect, self.rect_thickness)

        # Обновление кнопки "повернутися"
        self.return_button.update(self.screen)

        # Отрисовка содержимого, определяется дочерним классом
        self.draw_content()

    def handle_events(self, event):
        """Обработка событий."""
        if not self.is_visible:
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.return_button.checkForInput(pygame.mouse.get_pos()):
                self.hide()

        if event.type == pygame.MOUSEMOTION:
            self.return_button.changeColor(pygame.mouse.get_pos())

        # Обработка событий содержимого, определяется дочерним классом
        self.handle_content_events(event)

    @abstractmethod
    def draw_content(self):
        """Отрисовка содержимого меню. Реализуется в дочерних классах."""
        pass

    @abstractmethod
    def handle_content_events(self, event):
        """Обработка событий содержимого. Реализуется в дочерних классах."""
        pass



# Функция для создания эффекта плавного перехода (fade effect)
def fade_effect(SCREEN, duration=500, fade_in=True):
    fade_surface = pygame.Surface((1920, 1080))
    fade_surface.fill((0, 0, 0))

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    while True:
        elapsed_time = pygame.time.get_ticks() - start_time
        alpha = min(255, int(255 * elapsed_time / duration))

        if not fade_in:
            alpha = 255 - alpha

        fade_surface.set_alpha(alpha)
        SCREEN.blit(fade_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)

        if elapsed_time >= duration:
            break

# Функция для получения шрифта заданного размера
def get_font(size):
    return pygame.font.Font("assets/main_menu_font.otf", size)


