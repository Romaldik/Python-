import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UILabel, UIPanel, UISelectionList, UITextEntryLine
import sys


class ScreenManager:
    def __init__(self, screen):
        self.screen = screen
        self.ui_manager = pygame_gui.UIManager(screen.get_size(), theme_path="assets/theme.json")
        self.clock = pygame.time.Clock()
        self.current_screen = None
        self.screens = {
            "main_menu": self.main_menu_screen,
            "teams_menu": self.teams_menu_screen,
            "tournaments_menu": self.tournaments_menu_screen
        }
        self.switch_to("main_menu")

    def switch_to(self, screen_name):
        """Переключение экранов."""
        if self.current_screen:
            self.fade_effect(self.screen, fade_in=False)
            self.current_screen["window"].kill()
        self.current_screen = self.screens[screen_name]()
        self.fade_effect(self.screen, fade_in=True)

    def run(self):
        """Основной цикл приложения."""
        is_running = True
        while is_running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                self.ui_manager.process_events(event)
                if self.current_screen["handle_event"]:
                    self.current_screen["handle_event"](event)

            self.screen.fill((0, 0, 0))
            if self.current_screen["render_background"]:
                self.current_screen["render_background"]()
            self.ui_manager.update(time_delta)
            self.ui_manager.draw_ui(self.screen)
            pygame.display.update()

    @staticmethod
    def fade_effect(screen, duration=500, fade_in=True):
        """Эффект плавного появления/исчезновения."""
        fade_surface = pygame.Surface(screen.get_size())
        fade_surface.fill((0, 0, 0))
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        while True:
            elapsed_time = pygame.time.get_ticks() - start_time
            alpha = min(255, int(255 * elapsed_time / duration))

            if not fade_in:
                alpha = 255 - alpha

            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            clock.tick(60)

            if elapsed_time >= duration:
                break

    def main_menu_screen(self):
        """Главное меню."""
        window = UIPanel(
            pygame.Rect((0, 0), self.screen.get_size()),
            manager=self.ui_manager,
            object_id="#main_menu_panel"
        )

        UILabel(
            relative_rect=pygame.Rect((0, 20), (self.screen.get_width(), 50)),
            text="ГОЛОВНЕ МЕНЮ",
            manager=self.ui_manager,
            container=window,
            object_id="#main_menu_title"
        )

        buttons = [
            {"text": "Команди", "screen": "teams_menu"},
            {"text": "Турніри", "screen": "tournaments_menu"},
            {"text": "Вихід", "action": sys.exit}
        ]

        button_mapping = {}
        for i, button in enumerate(buttons):
            btn = UIButton(
                relative_rect=pygame.Rect(
                    (self.screen.get_width() // 2 - 100, 100 + i * 100), (200, 50)
                ),
                text=button["text"],
                manager=self.ui_manager,
                container=window,
                object_id="#menu_button"
            )
            button_mapping[btn] = button

        def handle_event(event):
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                user_data = button_mapping.get(event.ui_element)
                if user_data:
                    if "screen" in user_data:
                        self.switch_to(user_data["screen"])
                    elif "action" in user_data:
                        user_data["action"]()

        return {"window": window, "handle_event": handle_event, "render_background": None}

    def teams_menu_screen(self):
        """Меню команд."""
        window = UIPanel(
            pygame.Rect((0, 0), self.screen.get_size()),
            manager=self.ui_manager,
            object_id="#teams_menu_panel"
        )

        # Левый контейнер со списком команд
        selection_list = UISelectionList(
            relative_rect=pygame.Rect((20, 20), (200, self.screen.get_height() - 100)),
            item_list=["Команда 1", "Команда 2", "Команда 3"],
            manager=self.ui_manager,
            container=window
        )

        # Словарь данных для всех команд
        team_data = {
            "Команда 1": {"Игроки": ["арта", "миномёт", "танк"], "Коучи": ["скуф"], "Стаф": ["реклам агент"], "Спонсоры": ["офис президента"]},
            "Команда 2": {"Игроки": ["шмыг"], "Коучи": [], "Стаф": [], "Спонсоры": []},
            "Команда 3": {"Игроки": [], "Коучи": [], "Стаф": [], "Спонсоры": []},
        }

        # Центральный контейнер для списков
        center_container = UIPanel(
            pygame.Rect((240, 20), (540, self.screen.get_height() - 100)),
            manager=self.ui_manager,
            container=window,
            visible=False,
            object_id="#center_container"
        )

        # Переключатели
        tab_buttons = ["Игроки", "Коучи", "Стаф", "Спонсоры"]
        tabs = {}
        for i, tab in enumerate(tab_buttons):
            btn = UIButton(
                relative_rect=pygame.Rect((10 + i * 130, 10), (120, 40)),
                text=tab,
                manager=self.ui_manager,
                container=center_container
            )
            tabs[btn] = tab

        # Контейнеры для каждого списка
        list_containers = {}
        for tab_name in tab_buttons:
            list_container = UISelectionList(
                relative_rect=pygame.Rect((10, 60), (520, 360)),
                item_list=[],
                manager=self.ui_manager,
                container=center_container,
                visible=False
            )
            list_containers[tab_name] = list_container

        active_tab = None
        selected_team = None

        def switch_tab(tab_name):
            nonlocal active_tab
            if active_tab:
                list_containers[active_tab].hide()
            active_tab = tab_name
            list_containers[active_tab].show()
            if selected_team:
                list_containers[active_tab].set_item_list(team_data[selected_team][tab_name])

        def update_center_container(team_name):
            nonlocal selected_team
            selected_team = team_name
            if team_name:
                center_container.show()
                switch_tab("Игроки")
            else:
                center_container.hide()

        # Диалог добавления команды
        def show_add_team_dialog():
            # Создаём окно диалога
            dialog_window = UIPanel(
                pygame.Rect((self.screen.get_width() // 2 - 150, self.screen.get_height() // 2 - 100), (300, 200)),
                manager=self.ui_manager,
                object_id="#dialog_panel"
            )

            # Текстовая метка
            UILabel(
                relative_rect=pygame.Rect((10, 10), (280, 30)),
                text="Введите название команды:",
                manager=self.ui_manager,
                container=dialog_window
            )

            # Поле ввода текста
            input_field = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((10, 50), (280, 30)),
                manager=self.ui_manager,
                container=dialog_window
            )

            # Кнопки управления
            cancel_button = UIButton(
                relative_rect=pygame.Rect((30, 150), (100, 40)),
                text="Відмінити",
                manager=self.ui_manager,
                container=dialog_window,
                object_id="#cancel_button"
            )
            ok_button = UIButton(
                relative_rect=pygame.Rect((170, 150), (100, 40)),
                text="Ок",
                manager=self.ui_manager,
                container=dialog_window,
                object_id="#ok_button"
            )

            # Локальный цикл для обработки событий диалога
            dialog_active = True
            clock = pygame.time.Clock()

            while dialog_active:
                time_delta = clock.tick(60) / 1000.0

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    self.ui_manager.process_events(event)

                    if event.type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == cancel_button:
                            dialog_active = False
                        elif event.ui_element == ok_button:
                            new_team_name = input_field.get_text()
                            if new_team_name:
                                # Обновляем список через метод
                                selection_list.add_items([new_team_name])
                                team_data[new_team_name] = {tab: [] for tab in tab_buttons}

                            dialog_active = False


                # Обновляем UI-менеджер
                self.ui_manager.update(time_delta)

                # Рисуем интерфейс
                self.screen.fill((0, 0, 0))  # Заливка фона чёрным
                self.ui_manager.draw_ui(self.screen)
                pygame.display.update()

            # Уничтожаем окно диалога после завершения
            dialog_window.kill()


        # Кнопки внизу
        button_mapping = {}
        bottom_buttons = [
            {"text": "+", "action": show_add_team_dialog},
            {
                "text": "-",
                "action": lambda: remove_selected_team(selection_list.get_single_selection())
            }
        ]

        for i, btn_data in enumerate(bottom_buttons):
            btn = UIButton(
                relative_rect=pygame.Rect((20 + i * 60, self.screen.get_height() - 70), (50, 50)),
                text=btn_data["text"],
                manager=self.ui_manager,
                container=window
            )
            button_mapping[btn] = btn_data

        # Логика удаления команды
        def remove_selected_team(team_name):
            if team_name:
                selection_list.remove_items(team_name)
                del team_data[team_name]
                update_center_container(None)

        # Обработка событий
        def handle_event(event):
            nonlocal active_tab
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                # Обработка нижних кнопок
                user_data = button_mapping.get(event.ui_element)
                if user_data and "action" in user_data:
                    dialog_event = user_data["action"]()
                    if dialog_event:
                        handle_event(dialog_event)
                # Обработка переключателей
                if event.ui_element in tabs:
                    switch_tab(tabs[event.ui_element])

            elif event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                # Выделение команды из списка
                if event.ui_element == selection_list:
                    update_center_container(selection_list.get_single_selection())

        return {"window": window, "handle_event": handle_event, "render_background": None}

    def tournaments_menu_screen(self):
        """Меню турниров."""
        window = UIPanel(
            pygame.Rect((0, 0), self.screen.get_size()),
            manager=self.ui_manager,
            object_id="#tournaments_menu_panel"
        )

        selection_list = UISelectionList(
            relative_rect=pygame.Rect((20, 20), (200, self.screen.get_height() - 100)),
            item_list=["Турнир 1", "Турнир 2", "Турнир 3"],
            manager=self.ui_manager,
            container=window
        )

        button_mapping = {}
        bottom_buttons = [
            {"text": "Добавить", "action": lambda: selection_list.add_item(f"Турнир {len(selection_list.item_list) + 1}")},
            {"text": "Удалить", "action": lambda: selection_list.remove_item(selection_list.get_single_selection())}
        ]

        for i, btn_data in enumerate(bottom_buttons):
            btn = UIButton(
                relative_rect=pygame.Rect(
                    (240 + i * 100, self.screen.get_height() - 70), (90, 50)
                ),
                text=btn_data["text"],
                manager=self.ui_manager,
                container=window
            )
            button_mapping[btn] = btn_data

        def handle_event(event):
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                user_data = button_mapping.get(event.ui_element)
                if user_data and "action" in user_data:
                    user_data["action"]()

        return {"window": window, "handle_event": handle_event, "render_background": None}


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    app = ScreenManager(screen)
    app.run()
