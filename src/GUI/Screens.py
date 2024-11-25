import pygame, pygame_gui, sys
from pygame_gui.elements import UIButton, UILabel, UIPanel, UISelectionList, UITextEntryLine
from src.mypackage import Team, TeamMember, Player, Coach, Staff, Sponsor
from src.DataBase.db_utils import dbUtils

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
        team_data = Team.list_of_teams()
        for team in team_data:
            team.update({
                "players_list": Team.show_team_players(team["name"]) or [],
                "coaches_list": Team.show_team_coach(team["name"]) or [],
                "staff_list": Team.show_team_staff(team["name"]) or [],
                "sponsors_list": Team.show_sponsors(team["name"]) or []
            })

        def team_data_update():
            team_data[:] = Team.list_of_teams()
            for team in team_data:
                team.update({
                    "players_list": Team.show_team_players(team["name"]) or [],
                    "coaches_list": Team.show_team_coach(team["name"]) or [],
                    "staff_list": Team.show_team_staff(team["name"]) or [],
                    "sponsors_list": Team.show_sponsors(team["name"]) or []
                })

        # Функция для получения команды по имени
        def get_team_by_name(name):
            return next((team for team in team_data if team["name"] == name), None)

        # Функция для получения члена команды по имени
        def get_member_by_name(team, member_type, member_name):
            return next((member for member in team[member_type] if member["name"] == member_name), None)
        
        # Левый контейнер со списком команд
        selection_list = UISelectionList(
            relative_rect=pygame.Rect((20, 20), (200, self.screen.get_height() - 100)),
            item_list = [team["name"] for team in team_data if "name" in team],
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

        # Логика для вкладок
        tabs = []
        tab_mapping = {
            "Гравці": "players",
            "Тренери": "coaches",
            "Персонал": "staff",
            "Спонсори": "sponsors"
        }

        for i, (tab_name, tab_key) in enumerate(tab_mapping.items()):
            btn = UIButton(
                relative_rect=pygame.Rect((10 + i * 130, 10), (120, 40)),
                text=tab_name,
                manager=self.ui_manager,
                container=center_container,
                object_id=f"#tab_{tab_key}"
            )
            tabs.append(btn)

        # Контейнеры для списков участников
        list_containers = {
            tab_key: UISelectionList(
                relative_rect=pygame.Rect((10, 60), (520, center_container.rect.height - 140)),
                item_list=[],
                manager=self.ui_manager,
                container=center_container,
                visible=False
            )
            for tab_key in tab_mapping.values()
        }

        active_tab = "players"
        selected_team = None

        # Функция для переключения вкладок
        def switch_tab(tab_key):
            active_tab = tab_key
            print(active_tab)
            for key, list_container in list_containers.items():
                list_container.hide()
            if tab_key in list_containers:
                list_containers[tab_key].show()
                if selected_team:
                    team = get_team_by_name(selected_team)
                    print(team)
                    if team:
                        # Заполняем список участников для активной вкладки
                        list_containers[tab_key].set_item_list(
                            [member["name"] for member in team.get(f"{tab_key}_list", [])]
                        )
                        print(f"Tab: {tab_key}, Members: {team.get(f'{tab_key}_list', [])}")


        # Функция для обновления центрального контейнера
        def update_center_container(team_name):
            nonlocal selected_team
            selected_team = team_name
            if team_name:
                center_container.show()
                switch_tab("players")  # По умолчанию переключаемся на вкладку "Игроки"
            else:
                center_container.hide()

        def show_add_edit_member_dialog(active_tab, selected_member=None):
            """Диалог для добавления или редактирования члена команды."""
            dialog_window = UIPanel(
                pygame.Rect((self.screen.get_width() // 2 - 150, self.screen.get_height() // 2 - 120), (300, 240)),
                manager=self.ui_manager,
                starting_height=2
            )

            UILabel(
                relative_rect=pygame.Rect((10, 10), (280, 30)),
                text=f"Введите имя {active_tab}:",
                manager=self.ui_manager,
                container=dialog_window
            )

            input_field = pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((10, 50), (280, 30)),
                manager=self.ui_manager,
                container=dialog_window
            )

            # Если редактируем, заполняем поле текущим именем
            if selected_member:
                input_field.set_text(selected_member)

            cancel_button = UIButton(
                relative_rect=pygame.Rect((30, 180), (100, 40)),
                text="Отмена",
                manager=self.ui_manager,
                container=dialog_window
            )

            ok_button = UIButton(
                relative_rect=pygame.Rect((170, 180), (100, 40)),
                text="ОК",
                manager=self.ui_manager,
                container=dialog_window
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

                        if event.ui_element == ok_button:
                            new_member_name = input_field.get_text().strip()
                            if new_member_name:
                                if selected_team:
                                    team = Team(selected_team, None, None)
                                    if selected_member:
                                        # Редактирование члена
                                        if active_tab == "player":
                                            team.change_team_player(selected_member, new_member_name, selected_team)
                                        elif active_tab == "coach":
                                            team.change_team_coach(selected_member, new_member_name, selected_team)
                                        elif active_tab == "staff":
                                            team.change_team_staff(selected_member, new_member_name, selected_team)
                                    else:
                                        # Добавление нового члена   
                                        print("hujnaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                                        if active_tab == "player":
                                            print("ааааааааааааа")
                                            team.add_player(new_member_name, selected_team)
                                            print("FFFFFFFFFFFFF")
                                        elif active_tab == "coach":
                                            team.add_coach(new_member_name, selected_team)
                                        elif active_tab == "staff":
                                            team.add_staff(new_member_name, selected_team)

                                    # Обновляем данные и интерфейс
                                    team_data_update()
                                    update_center_container(selected_team)

                            dialog_window.kill()
                            dialog_active = False

                self.ui_manager.update(time_delta)
                self.screen.fill((0, 0, 0))  # Заливка фона чёрным
                self.ui_manager.draw_ui(self.screen)
                pygame.display.update()
                
        def delete_selected_member():
            if not active_tab or not selected_team:
                return

            team = get_team_by_name(selected_team)
            if not team:
                return

            selected_item = list_containers[active_tab].get_single_selection()
            if selected_item:
                member = get_member_by_name(team, f"{active_tab}_list", selected_item)
                if member:
                    team[f"{active_tab}_list"].remove(member)
                    switch_tab(active_tab)

        # --- Внутренняя функция для диалога ---
        def show_add_team_dialog():
            """Диалог добавления команды."""

            # Создание компонентов диалога
            dialog_window = UIPanel(
                pygame.Rect((self.screen.get_width() // 2 - 150, self.screen.get_height() // 2 - 80), (300, 200)),
                manager=self.ui_manager,
                starting_height=2
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
                container=dialog_window
            )
            ok_button = UIButton(
                relative_rect=pygame.Rect((170, 150), (100, 40)),
                text="ОК",
                manager=self.ui_manager,
                container=dialog_window
            )

            # Локальная переменная для отслеживания активности диалога
            dialog_active = True

            # Обработчик событий для диалога
            def handle_dialog_event(event):
                nonlocal dialog_active
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == cancel_button:
                        dialog_window.kill()
                        dialog_active = False
                    elif event.ui_element == ok_button:
                        new_team_name = input_field.get_text()
                        if new_team_name:
                            # Создаём новую команду
                            team = Team(name=new_team_name, location="Unknown", period_of_sponsorship="unknown amount of days")
                            team.create_team()
                            team_data_update()
                            
                            # Обновляем интерфейс
                            selection_list.add_items([new_team_name])
                            team_data.append({
                                "name": new_team_name,
                                "players_list": [],
                                "coaches_list": [],
                                "staff_list": [],
                                "sponsors_list": []
                            })
                        dialog_window.kill()
                        dialog_active = False

            return handle_dialog_event, lambda: dialog_active
        
        # Удаление выбранной команды
        def remove_selected_team(team_name):
            """Удаляет выбранную команду."""
            if team_name:
                selection_list.remove_items([team_name])  # Удаляем из интерфейса
                Team.delete_team(get_team_by_name(team_name))
                team_data_update()
                update_center_container(None)  # Обновляем центральный контейнер

        # Кнопки
        button_mapping = {}

        team_buttons = [
            {"text": "+", "action": show_add_team_dialog},
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
            {"text": "Додати", "action": lambda: show_add_edit_member_dialog(active_tab)},
            {
                "text": "Редагувати",
                "action": lambda: (
                    show_add_edit_member_dialog(
                        active_tab, 
                        list_containers[active_tab].get_single_selection()  # Получение имени выбранного участника
                    )
                    if active_tab and selected_team and list_containers[active_tab].get_single_selection() 
                    else None
                )
            },
            {"text": "Видалити", "action": lambda: delete_selected_member()},
            {"text": "Повернутися", "action": lambda: self.switch_to("main_menu")}
        ]

        for i, btn_data in enumerate(center_bottom_buttons):
            btn = UIButton(
                relative_rect=pygame.Rect((10 + i * 130, center_container.rect.height - 60), (120, 40)),
                text=btn_data["text"],
                manager=self.ui_manager,
                container=center_container
            )
            button_mapping[btn] = btn_data["action"]

            # --- Основной цикл обработки событий ---
        
        dialog_handler = None  # Обработчик событий диалога
        is_dialog_active = lambda: False  # Проверка активности диалога

        def handle_event(event):
            nonlocal dialog_handler, is_dialog_active

            if is_dialog_active():  # Если активен диалог, обрабатываем его
                dialog_handler(event)
            else:  # Иначе обрабатываем другие события
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    action = button_mapping.get(event.ui_element)
                    if action:
                        if event.ui_element.text == "+":  # Если добавляем команду
                            dialog_handler, is_dialog_active = show_add_team_dialog()
                        else:
                            action()
                    else:
                        # Проверяем, нажата ли одна из кнопок вкладок
                        for i, tab_button in enumerate(tabs):
                            if event.ui_element == tab_button:
                                # Переключаемся на вкладку по индексу
                                tab_key = list(tab_mapping.values())[i]
                                switch_tab(tab_key)
                                break

                elif event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                    # Обработка выбора команды
                    selected_item = selection_list.get_single_selection()
                    if selected_item:
                        update_center_container(selected_item)


        return {"window": window, "handle_event": handle_event, "render_background": None}
    
    def tournaments_menu_screen(self):
        """Меню турнірів."""
        window = UIPanel(
            pygame.Rect((0, 0), self.screen.get_size()),
            manager=self.ui_manager,
            object_id="#tournaments_menu_panel"
        )

        # Список турнірів за замовчуванням
        tournament_data = {
            "Турнір 1": "Інформація про Турнір 1: дата, місце проведення, учасники...",
            "Турнір 2": "Інформація про Турнір 2: дата, місце проведення, учасники...",
            "Турнір 3": "Інформація про Турнір 3: дата, місце проведення, учасники..."
        }

        selection_list = UISelectionList(
            relative_rect=pygame.Rect((20, 20), (200, self.screen.get_height() - 100)),
            item_list=list(tournament_data.keys()),  # Використовуємо тільки назви турнірів
            manager=self.ui_manager,
            container=window
        )

        # Панель для відображення інформації про вибраний турнір
        info_panel = UIPanel(
            pygame.Rect((240, 20), (self.screen.get_width() - 260, self.screen.get_height() - 100)),
            manager=self.ui_manager,
            container=window
        )

        info_label = UILabel(
            relative_rect=pygame.Rect((10, 10), (info_panel.rect.width - 20, info_panel.rect.height - 20)),
            text="Виберіть турнір для перегляду інформації.",
            manager=self.ui_manager,
            container=info_panel
        )

        button_mapping = {}

        def show_add_tournament_dialog():
            """Открывает диалог для добавления нового турнира."""
            dialog_window = UIPanel(
                pygame.Rect((self.screen.get_width() // 2 - 150, self.screen.get_height() // 2 - 100), (300, 200)),
                manager=self.ui_manager,
                starting_height=2,
                object_id="#dialog_panel"
            )

            UILabel(
                relative_rect=pygame.Rect((10, 10), (280, 30)),
                text="Введите имя турнира:",
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
                container=dialog_window
            )

            ok_button = UIButton(
                relative_rect=pygame.Rect((170, 150), (100, 40)),
                text="ОК",
                manager=self.ui_manager,
                container=dialog_window
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
                        elif event.ui_element == ok_button:
                            new_tournament_name = input_field.get_text()
                            if new_tournament_name:
                                tournament_data[new_tournament_name] = f"Информация о {new_tournament_name}..."
                                selection_list.add_items([new_tournament_name])
                                info_label.set_text(f"Турнир {new_tournament_name} добавлен.")
                            dialog_window.kill()
                            dialog_active = False

                self.ui_manager.update(time_delta)
                self.screen.fill((0, 0, 0))
                self.ui_manager.draw_ui(self.screen)
                pygame.display.update()

        def remove_tournament():
            """Функция для удаления выбранного турнира."""
            selected_tournament = selection_list.get_single_selection()
            if selected_tournament:
                del tournament_data[selected_tournament]
                selection_list.remove_items(selected_tournament)
                info_label.set_text(f"Турнир {selected_tournament} удалён.")

        bottom_buttons = [
            {"text": "Добавить", "action": show_add_tournament_dialog},
            {"text": "Удалить", "action": remove_tournament},
            {"text": "Назад", "action": lambda: self.switch_to("main_menu")}
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
            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION and event.ui_element == selection_list:
                selected_tournament = selection_list.get_single_selection()
                if selected_tournament:
                    info_label.set_text(tournament_data[selected_tournament])
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                user_data = button_mapping.get(event.ui_element)
                if user_data and "action" in user_data:
                    user_data["action"]()

        return {"window": window, "handle_event": handle_event, "render_background": None}


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1040, 786))
    app = ScreenManager(screen)
    app.run()
