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
        # Основное окно
        window = UIPanel(
            pygame.Rect((0, 0), self.screen.get_size()),
            manager=self.ui_manager,
            object_id="#teams_menu_panel"
        )

        # Словарь данных для всех команд
        team_data = {
            "Команда 1": {"Игроки": ["Арта", "Миномёт", "Танк"], "Коучи": ["Скуф"], "Стаф": ["Рекламный агент"], "Спонсоры": ["Офис Президента"]},
            "Команда 2": {"Игроки": ["Шмыг"], "Коучи": [], "Стаф": [], "Спонсоры": []},
            "Команда 3": {"Игроки": [], "Коучи": [], "Стаф": [], "Спонсоры": []},
        }

        # Левый контейнер со списком команд
        selection_list = UISelectionList(
            relative_rect=pygame.Rect((20, 20), (200, self.screen.get_height() - 100)),
            item_list=list(team_data.keys()),
            manager=self.ui_manager,
            container=window
        )

        # Центральный контейнер для списков
        center_container = UIPanel(
            pygame.Rect((240, 20), (540, self.screen.get_height() - 100)),
            manager=self.ui_manager,
            container=window,
            visible=False,
            object_id="#center_container"
        )

        # Кнопки вкладок
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

        # Контейнеры списков для участников
        list_containers = {}
        for tab_name in tab_buttons:
            list_containers[tab_name] = UISelectionList(
                relative_rect=pygame.Rect((10, 60), (520, center_container.rect.height - 140)),
                item_list=[],
                manager=self.ui_manager,
                container=center_container,
                visible=False
            )

        active_tab = "Игроки"
        selected_team = None

        # Функция для переключения вкладок
        def switch_tab(tab_name):
            nonlocal active_tab
            if active_tab:
                list_containers[active_tab].hide()
            active_tab = tab_name
            list_containers[active_tab].show()
            if selected_team:
                list_containers[active_tab].set_item_list(team_data[selected_team][tab_name])

        # Функция для обновления центрального контейнера
        def update_center_container(team_name):
            nonlocal selected_team
            selected_team = team_name
            if team_name:
                center_container.show()
                switch_tab("Игроки")
            else:
                center_container.hide()

        # Диалог добавления/редактирования участника
        def show_add_edit_member_dialog(member_type, existing_member_name=None):

            dialog_window0 = UIPanel(
                pygame.Rect((self.screen.get_width() // 2 - 150, self.screen.get_height() // 2 - 120), (300, 200)),
                manager=self.ui_manager,
                starting_height=2,
                object_id="#dialog_panel0"
            )

            UILabel(
                relative_rect=pygame.Rect((10, 10), (280, 30)),
                text=f"Введите имя {member_type}:",
                manager=self.ui_manager,
                container=dialog_window0
            )

            input_field = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((10, 50), (280, 30)),
                manager=self.ui_manager,
                container=dialog_window0
            )
            if existing_member_name:
                input_field.set_text(existing_member_name)

            cancel_button = UIButton(
                relative_rect=pygame.Rect((30, 150), (100, 40)),
                text="Отмена",
                manager=self.ui_manager,
                container=dialog_window0
            )
            OK_button = UIButton(
                relative_rect=pygame.Rect((170, 150), (100, 40)),
                text="ОК",
                manager=self.ui_manager,
                container=dialog_window0
            )

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
                            dialog_window0.kill()
                            dialog_active = False
                        elif event.ui_element == OK_button:
                            new_name = input_field.get_text()
                            if new_name:
                                if existing_member_name:
                                    member_list = team_data[selected_team][member_type]
                                    member_list[member_list.index(existing_member_name)] = new_name
                                else:
                                    team_data[selected_team][member_type].append(new_name)
                                dialog_window0.kill()
                                dialog_active = False
                                switch_tab(member_type)
                                break

                self.ui_manager.update(time_delta)
                self.screen.fill((0, 0, 0))
                self.ui_manager.draw_ui(self.screen)
                pygame.display.update()

        # Кнопки управления участниками
        def delete_selected_member():
            if active_tab and selected_team:
                selected_item = list_containers[active_tab].get_single_selection()
                if selected_item:
                    team_data[selected_team][active_tab].remove(selected_item)
                    switch_tab(active_tab)

        # Диалог добавления команды
        def show_add_team_dialog():
            """Отображает диалог для добавления новой команды."""
            dialog_window = UIPanel(
                pygame.Rect((self.screen.get_width() // 2 - 150, self.screen.get_height() // 2 - 80), (300, 200)),
                manager=self.ui_manager,
                starting_height=1,
                object_id="#dialog_panel"
            )

            UILabel(
                relative_rect=pygame.Rect((10, 10), (280, 30)),
                text="Введите название команды:",
                manager=self.ui_manager,
                container=dialog_window
            )

            input_field = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((10, 50), (280, 30)),
                manager=self.ui_manager,
                container=dialog_window
            )

            cancel_button = UIButton(
                relative_rect=pygame.Rect((30, 150), (100, 40)),
                text="Отмена",
                manager=self.ui_manager,
                container=dialog_window,
                object_id="#cancel_button"
            )

            OK_button = UIButton(
                relative_rect=pygame.Rect((170, 150), (100, 40)),
                text="ОК",
                manager=self.ui_manager,
                container=dialog_window,
                object_id="#ok_button"
            )

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
                            dialog_window.kill()
                            dialog_active = False
                        elif event.ui_element == OK_button:
                            new_team_name = input_field.get_text()
                            if new_team_name:
                                # Добавляем новую команду в список
                                selection_list.add_items([new_team_name])
                                team_data[new_team_name] = {tab: [] for tab in ["Игроки", "Коучи", "Стаф", "Спонсоры"]}
                            dialog_window.kill()
                            dialog_active = False
                            break

                self.ui_manager.update(time_delta)
                self.screen.fill((0, 0, 0))  # Заливка фона чёрным
                self.ui_manager.draw_ui(self.screen)
                pygame.display.update()

        # Удаление выбранной команды
        def remove_selected_team(team_name):
            """Удаляет выбранную команду."""
            if team_name:
                selection_list.remove_items([team_name])  # Удаляем из интерфейса
                del team_data[team_name]  # Удаляем из данных
                update_center_container(None)  # Обновляем центральный контейнер

        # Кнопки
        button_mapping = {}

        team_buttons = [
            {"text": "+", "action": lambda: show_add_team_dialog()},
            {"text": "-", "action": lambda: remove_selected_team(selection_list.get_single_selection())}
        ]

        for i, btn_data in enumerate(team_buttons):
            btn = UIButton(
                relative_rect=pygame.Rect((20 + i * 60, self.screen.get_height() - 70), (50, 50)),
                text=btn_data["text"],
                manager=self.ui_manager,
                container=window
            )
            button_mapping[btn] = btn_data["action"]

        center_bottom_buttons = [
            {"text": "Добавить", "action": lambda: show_add_edit_member_dialog(active_tab)},
            {"text": "Редактировать", "action": lambda: show_add_edit_member_dialog(active_tab)},
            {"text": "Удалить", "action": lambda: delete_selected_member()},
            {"text": "Назад", "action": lambda: self.switch_to("main_menu")}
        ]

        for i, btn_data in enumerate(center_bottom_buttons):
            btn = UIButton(
                relative_rect=pygame.Rect((10 + i * 130, center_container.rect.height - 60), (120, 40)),
                text=btn_data["text"],
                manager=self.ui_manager,
                container=center_container
            )
            button_mapping[btn] = btn_data["action"]

        def handle_event(event):
            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION and event.ui_element == selection_list:
                update_center_container(selection_list.get_single_selection())
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                action = button_mapping.get(event.ui_element)
                if action:
                    action()
                if event.ui_element in tabs:
                    switch_tab(tabs[event.ui_element])

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
    screen = pygame.display.set_mode((1040, 786))
    app = ScreenManager(screen)
    app.run()
