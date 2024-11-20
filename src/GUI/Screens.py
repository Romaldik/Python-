from src.mypackage import *
from src.DataBase.db_utils import dbUtils as db
from abc import ABC, abstractmethod
import pygame, pygame_gui, sys


class ScreenManager:
    def __init__(self, screen):
        self.screen = screen
        self.ui_manager = pygame_gui.UIManager(screen.get_size())  # Создание UIManager
        self.clock = pygame.time.Clock()
        self.current_screen_name = "main_menu"
        self.screens = {
            "main_menu": MainMenu(screen, self.ui_manager, self),
            "teams_menu": TeamsMenu(screen, self.ui_manager, self),
            "tournaments_menu": TournamentsMenu(screen, self.ui_manager, self),
        }
        self.active_container = None
        self.switch_to(self.current_screen_name)

    def switch_to(self, screen_name):
        """Переключение экранов."""
        if self.active_container:
            self.active_container.kill()  # Удаление активного контейнера
        self.current_screen_name = screen_name
        self.active_container = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), self.screen.get_size()),
            starting_height=0,
            manager=self.ui_manager
        )
        self.screens[screen_name].load_into_container(self.active_container)

    def run(self):
        """Основной цикл программы."""
        is_running = True
        while is_running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                self.ui_manager.process_events(event)
                self.screens[self.current_screen_name].handle_event(event)

            # Отображение текущего экрана
            self.screens[self.current_screen_name].render_background()
            self.ui_manager.update(time_delta)
            self.ui_manager.draw_ui(self.screen)

            pygame.display.update()


class MainMenu:
    def __init__(self, screen, ui_manager, manager):
        self.screen = screen
        self.background = pygame.image.load("assets/Background.png")  # Фон главного меню
        self.ui_manager = ui_manager
        self.manager = manager

    def load_into_container(self, container):
        """Загрузка элементов главного меню в контейнер."""
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (self.screen.get_width(), 100)),
            text="ГОЛОВНЕ МЕНЮ",
            manager=self.ui_manager,
            container=container,
            object_id="#menu_title"
        )

        button_width, button_height = 400, 100
        button_spacing = 50
        center_x = self.screen.get_width() // 2 - button_width // 2
        start_y = 150

        self.teams_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x, start_y), (button_width, button_height)),
            text="Команди",
            manager=self.ui_manager,
            container=container
        )
        self.tournaments_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x, start_y + button_height + button_spacing), (button_width, button_height)),
            text="Турніри",
            manager=self.ui_manager,
            container=container
        )
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x, start_y + 2 * (button_height + button_spacing)), (button_width, button_height)),
            text="Вихід",
            manager=self.ui_manager,
            container=container
        )

    def handle_event(self, event):
        """Обработка событий главного меню."""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.teams_button:
                self.manager.switch_to("teams_menu")
            elif event.ui_element == self.tournaments_button:
                self.manager.switch_to("tournaments_menu")
            elif event.ui_element == self.quit_button:
                pygame.quit()
                sys.exit()

    def render_background(self):
        """Отображение фона."""
        self.screen.blit(self.background, (0, 0))


class TeamsMenu:
    def __init__(self, screen, ui_manager, manager):
        self.screen = screen
        self.background = pygame.image.load("assets/TeamsBackground.png")
        self.ui_manager = ui_manager
        self.manager = manager
        self.team_buttons = []
        self.selected_team = None
        self.selected_category = "Гравці"

    def load_into_container(self, container):
        """Загрузка элементов меню команд в контейнер."""
        # Фон
        self.background_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), self.screen.get_size()),
            starting_height=0,
            manager=self.ui_manager,
            container=container,
            object_id="#background_panel"
        )
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 20, 400, 50),
            text="Команди",
            manager=self.ui_manager,
            container=self.background_panel,
            object_id="#title_label"
        )

        # Кнопка назад
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(20, 100, 200, 50),
            text="Назад",
            manager=self.ui_manager,
            container=self.background_panel
        )

        # Прокручиваемый список команд
        self.scrollable_team_list = pygame_gui.elements.UIScrollingContainer(
            relative_rect=pygame.Rect(20, 180, 300, 400),
            manager=self.ui_manager,
            container=self.background_panel
        )
        self.update_team_list(self.scrollable_team_list)

        # Прокручиваемый контейнер для отображения членов команды
        self.scrollable_container = pygame_gui.elements.UIScrollingContainer(
            relative_rect=pygame.Rect(350, 180, 700, 400),
            manager=self.ui_manager,
            container=self.background_panel
        )

        # Категории
        self.category_buttons = []
        categories = ["Гравці", "Коучі", "Спонсори", "Інші"]
        for i, category in enumerate(categories):
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(400 + i * 150, 100, 140, 40),
                text=category,
                manager=self.ui_manager,
                container=self.background_panel
            )
            self.category_buttons.append((button, category))

        # Поле ввода и кнопки для добавления/удаления команды
        self.input_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(20, 600, 300, 40),
            manager=self.ui_manager,
            container=self.background_panel
        )
        self.input_box.visible = False

        self.add_team_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(20, 660, 140, 40),
            text="Додати",
            manager=self.ui_manager,
            container=self.background_panel
        )
        self.remove_team_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(180, 660, 140, 40),
            text="Видалити",
            manager=self.ui_manager,
            container=self.background_panel
        )
        self.save_new_team_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(20, 720, 300, 40),
            text="Зберегти",
            manager=self.ui_manager,
            container=self.background_panel
        )
        self.save_new_team_button.visible = False

    def update_team_list(self, container):
        """Обновляет список команд в контейнере."""
        for element in container.get_container().elements:
            element.kill()

        self.team_buttons = []
        self.teams = Team.list_of_teams() or []

        for i, team in enumerate(self.teams):
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(0, i * 50, 280, 40),
                text=team["name"],
                manager=self.ui_manager,
                container=container.get_container()
            )
            self.team_buttons.append((button, team))

    def display_team_members(self, container):
        """Обновляет содержимое прокручиваемого контейнера для выбранной команды и категории."""
        for element in container.get_container().elements:
            element.kill()

        if self.selected_team:
            if self.selected_category == "Гравці":
                members = Team.show_team_players(self.selected_team["name"])
            elif self.selected_category == "Коучі":
                members = Team.show_team_coaches(self.selected_team["name"])
            elif self.selected_category == "Спонсори":
                members = Team.show_team_sponsors(self.selected_team["name"])
            elif self.selected_category == "Інші":
                members = Team.show_team_other(self.selected_team["name"])
            else:
                members = []

            for i, member in enumerate(members):
                pygame_gui.elements.UILabel(
                    relative_rect=pygame.Rect(0, i * 30, 680, 30),
                    text=f"{member[0]} {member[1]} {member[2]} {member[3]}",
                    manager=self.ui_manager,
                    container=container.get_container()
                )

    def handle_event(self, event):
        """Обработка событий меню команд."""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.back_button:
                self.manager.switch_to("main_menu")

            if event.ui_element == self.add_team_button:
                self.input_box.visible = True
                self.save_new_team_button.visible = True

            if event.ui_element == self.save_new_team_button:
                new_team_name = self.input_box.get_text()
                if new_team_name:
                    Team.create_team(new_team_name)
                    self.update_team_list(self.scrollable_team_list)
                    self.input_box.set_text("")
                    self.input_box.visible = False
                    self.save_new_team_button.visible = False

            if event.ui_element == self.remove_team_button and self.selected_team:
                Team.delete_team(self.selected_team["name"])
                self.update_team_list(self.scrollable_team_list)
                self.selected_team = None

            for button, team in self.team_buttons:
                if event.ui_element == button:
                    self.selected_team = team
                    self.display_team_members(self.scrollable_container)

            for button, category in self.category_buttons:
                if event.ui_element == button:
                    self.selected_category = category
                    self.display_team_members(self.scrollable_container)

    def render_background(self):
        """Отображение фона."""
        self.screen.blit(self.background, (0, 0))


class TournamentsMenu:
    def __init__(self, screen, ui_manager, manager):
        self.screen = screen
        self.background = pygame.image.load("assets/TournamentsBackground.png")  # Фон меню турниров
        self.ui_manager = ui_manager
        self.manager = manager

        # Пример данных для списка турниров
        self.tournaments_list = [
            {"name": "Турнір 1", "location": "Київ", "prize_fund": "5000", "status": "Скоро почнеться", "start_date": "2024-12-01", "end_date": "2024-12-05"},
            {"name": "Турнір 2", "location": "Львів", "prize_fund": "10000", "status": "Триває", "start_date": "2024-11-20", "end_date": "2024-11-25"},
        ]

    def load_into_container(self, container):
        """Загрузка элементов меню турниров в контейнер."""
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (self.screen.get_width(), 100)),
            text="МЕНЮ ТУРНІРІВ",
            manager=self.ui_manager,
            container=container,
            object_id="#menu_title"
        )

        button_width, button_height = 400, 100
        button_spacing = 50
        center_x = self.screen.get_width() // 2 - button_width // 2
        start_y = 150

        self.add_tournament_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x, start_y), (button_width, button_height)),
            text="Додати турнір",
            manager=self.ui_manager,
            container=container
        )
        self.delete_tournament_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x, start_y + button_height + button_spacing), (button_width, button_height)),
            text="Видалити турнір",
            manager=self.ui_manager,
            container=container
        )
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x, start_y + 2 * (button_height + button_spacing)), (button_width, button_height)),
            text="Назад",
            manager=self.ui_manager,
            container=container
        )

        # Отображение списка турниров
        list_start_y = 150 + 3 * (button_height + button_spacing)
        for i, tournament in enumerate(self.tournaments_list):
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((50, list_start_y + i * 50), (self.screen.get_width() - 100, 40)),
                text=f"{tournament['name']}, {tournament['location']}, Призовий фонд: {tournament['prize_fund']}, "
                     f"Статус: {tournament['status']}, Початок: {tournament['start_date']}, Кінець: {tournament['end_date']}",
                manager=self.ui_manager,
                container=container
            )

    def handle_event(self, event):
        """Обработка событий меню турниров."""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.add_tournament_button:
                print("Добавление турнира")
            elif event.ui_element == self.delete_tournament_button:
                print("Удаление турнира")
            elif event.ui_element == self.back_button:
                self.manager.switch_to("main_menu")

    def render_background(self):
        """Отображение фона."""
        self.screen.blit(self.background, (0, 0))


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


