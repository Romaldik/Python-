
import pygame, sys
from GUI.button import Button
from GUI.Dropdown import Dropdown
from GUI.inputBox import InputBox

import sqlite3
from __init__ import Team, Coach, Sponsor, Tournament, TeamMember, Staff, Player, TrainingProgram


# SQLite database setup
conn = sqlite3.connect('esports_manager.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS teams (id INTEGER PRIMARY KEY, name TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, role TEXT, team_id INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS staff (id INTEGER PRIMARY KEY, name TEXT, position TEXT, team_id INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS tournaments (
                id INTEGER PRIMARY KEY, 
                name TEXT, 
                location TEXT, 
                date TEXT, 
                prize_fund INTEGER,
                status TEXT,
                start_date TEXT,
                end_date TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS training_programs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                duration INTEGER,
                focus_area TEXT,
                team_id INTEGER,
                FOREIGN KEY (team_id) REFERENCES teams(id))''')

conn.commit()

# Графічний інтерфес
pygame.init()

SCREEN = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Кіберспортивний менеджер")

# Завантаження фонових зображень
BG = pygame.image.load("assets/Background.png")
BG_TEAMS = pygame.image.load("assets/TeamsBackground.png")

# Повертає об'єкт типу "шрифт" певного розміру для подальшого використання
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/main_menu_font.otf", size)

# Створює візуальний еффект "fade" у вікні програми для переходів
def fade_effect(duration=500, fade_in=True):
    fade_surface = pygame.Surface((1920, 1080))
    fade_surface.fill((0, 0, 0))
    
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    while True:
        elapsed_time = pygame.time.get_ticks() - start_time
        alpha = min(255, int(255 * elapsed_time / duration))
        
        if not fade_in:  # Если не затухание, убираем цвет
            alpha = 255 - alpha

        fade_surface.set_alpha(alpha)
        SCREEN.blit(fade_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)

        if elapsed_time >= duration:
            break


def teams_menu():
    fade_effect(duration=300, fade_in=True)

    # Создание полей для ввода имени и выпадающих списков
    input_boxes = [InputBox(20, 100 + i * 60, 140, 40) for i in range(5)]
    roles_dropdowns = [Dropdown(180, 100 + i * 60, ["Снайпер", "Капитан", "Игрок на оупен"]) for i in range(5)]
    skill_level_dropdowns = [Dropdown(380, 100 + i * 60, [str(i) for i in range(1, 11)]) for i in range(5)]

    while True:
        SCREEN.blit(BG_TEAMS, (0, 0))

        TEAMS_MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Заголовок
        TITLE_TEXT = get_font(75).render("Команди", True, "White")
        TITLE_RECT = TITLE_TEXT.get_rect(topleft=(20, 20))
        SCREEN.blit(TITLE_TEXT, TITLE_RECT)

        # Список команд
        teams_list = ["Команда 1", "Команда 2", "Команда 3"]  # Пример списка команд
        for i, team in enumerate(teams_list):
            TEAM_TEXT = get_font(50).render(team, True, "White")
            TEAM_RECT = TEAM_TEXT.get_rect(topleft=(20, 100 + i * 60))
            SCREEN.blit(TEAM_TEXT, TEAM_RECT)
            # Логика для выделения области команды при наведении
            if TEAM_RECT.collidepoint(TEAMS_MENU_MOUSE_POS):
                pygame.draw.rect(SCREEN, (100, 100, 100), TEAM_RECT)  # Подсветка области

        # Кнопки справа
        ADD_TEAM_BUTTON = Button(image=None, pos=(1200, 200),
                                 text_input="Додати нову команду", font=get_font(50), base_color="White", hovering_color="Green")
        EDIT_TEAM_BUTTON = Button(image=None, pos=(1200, 300),
                                  text_input="Редагувати команду", font=get_font(50), base_color="White", hovering_color="Green")
        DELETE_TEAM_BUTTON = Button(image=None, pos=(1200, 400),
                                    text_input="Видалити команду", font=get_font(50), base_color="White", hovering_color="Green")

        ADD_TEAM_BUTTON.changeColor(TEAMS_MENU_MOUSE_POS)
        ADD_TEAM_BUTTON.update(SCREEN)
        EDIT_TEAM_BUTTON.changeColor(TEAMS_MENU_MOUSE_POS)
        EDIT_TEAM_BUTTON.update(SCREEN)
        DELETE_TEAM_BUTTON.changeColor(TEAMS_MENU_MOUSE_POS)
        DELETE_TEAM_BUTTON.update(SCREEN)

        # Область для заполнения информации о команде
        details_area_rect = pygame.Rect(650, 100, 500, 600)  # Прямоугольник области
        pygame.draw.rect(SCREEN, (0, 0, 0, 200), details_area_rect)  # Полупрозрачный черный прямоугольник
        # Логика для отображения полей для ввода имени команды и участников

        # Кнопки "Зберегти" и "Скасувати"
        SAVE_BUTTON = Button(image=None, pos=(800, 750),
                             text_input="Зберегти", font=get_font(50), base_color="White", hovering_color="Green")
        CANCEL_BUTTON = Button(image=None, pos=(1100, 750),
                               text_input="Скасувати", font=get_font(50), base_color="White", hovering_color="Green")
        GO_BACK_BUTTON = Button(image=None, pos=(1100, 950),
                               text_input="Повернутися", font=get_font(50), base_color="White", hovering_color="Green")

        SAVE_BUTTON.changeColor(TEAMS_MENU_MOUSE_POS)
        SAVE_BUTTON.update(SCREEN)
        CANCEL_BUTTON.changeColor(TEAMS_MENU_MOUSE_POS)
        CANCEL_BUTTON.update(SCREEN)
        GO_BACK_BUTTON.changeColor(TEAMS_MENU_MOUSE_POS)
        GO_BACK_BUTTON.update(SCREEN)

        for i in range(5):
            input_boxes[i].draw(SCREEN)
            roles_dropdowns[i].draw(SCREEN)
            skill_level_dropdowns[i].draw(SCREEN)


        for event in pygame.event.get():
            # Отображение игроков и управление событиями
            for i in range(5):
                input_boxes[i].handle_event(event)
                roles_dropdowns[i].handle_event(event)
                skill_level_dropdowns[i].handle_event(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if GO_BACK_BUTTON.checkForInput(TEAMS_MENU_MOUSE_POS):
                    main_menu()
                # Логика для обработки нажатия кнопок "Додати нову команду", "Редагувати команду" и "Видалити команду"
                if ADD_TEAM_BUTTON.checkForInput(TEAMS_MENU_MOUSE_POS):
                    # Здесь должна быть логика для добавления новой команды
                    pass
                if EDIT_TEAM_BUTTON.checkForInput(TEAMS_MENU_MOUSE_POS):
                    # Здесь должна быть логика для редактирования команды
                    pass
                if DELETE_TEAM_BUTTON.checkForInput(TEAMS_MENU_MOUSE_POS):
                    # Здесь должна быть логика для удаления команды
                    pass
                if SAVE_BUTTON.checkForInput(TEAMS_MENU_MOUSE_POS):
                    # Здесь должна быть логика для сохранения изменений
                    pass
                if CANCEL_BUTTON.checkForInput(TEAMS_MENU_MOUSE_POS):
                    # Здесь должна быть логика для отмены изменений
                    pass

        pygame.display.update()


def tournaments_menu():
    while True:
        TEAMS_MENU_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the Teams screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(TEAMS_MENU_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(TEAMS_MENU_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    fade_effect(duration=300, fade_in=True)
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("ГОЛОВНЕ МЕНЮ", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(500, 100))

        TEAMS_BUTTON = Button(image=pygame.image.load("assets/Teams Rect.png"), pos=(500, 350), 
                            text_input="Команди", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        TOURNAMENTS_BUTTON = Button(image=pygame.image.load("assets/Tournaments Rect.png"), pos=(500, 550), 
                            text_input="Турнiри", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(500, 800), 
                            text_input="Вихiд", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [TEAMS_BUTTON, TOURNAMENTS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if TEAMS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    teams_menu()
                if TOURNAMENTS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    tournaments_menu()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

""" # Додавання команли
def add_team_window(root):
    add_window = tk.Toplevel(root)
    add_window.title("Додати команду")
    
    add_window.geometry("800x800+500+100")
    
    tk.Label(add_window, text="Назва команди").pack()
    entry_team_name = tk.Entry(add_window)
    entry_team_name.pack()
    
    tk.Label(add_window, text="Тренер").pack()
    entry_coach_name = tk.Entry(add_window)
    entry_coach_name.pack()
    
    players = []
    tk.Label(add_window, text="Учасники команди").pack()

    player_frame = tk.Frame(add_window)
    player_frame.pack()
    
    tk.Label(player_frame, text="Ім'я").grid(row=0, column=0)
    tk.Label(player_frame, text="Роль").grid(row=0, column=1)
    tk.Label(player_frame, text="Рівень").grid(row=0, column=2)

    for i in range(5):
        frame = tk.Frame(add_window)
        frame.pack()
        tk.Label(frame, text=f"Гравець {i+1}").grid(row=0, column=0)
        player_name = tk.Entry(frame)
        player_name.grid(row=0, column=1)
        player_role = tk.Entry(frame)
        player_role.grid(row=0, column=2)
        player_level = tk.Entry(frame)
        player_level.grid(row=0, column=3)
        players.append((player_name, player_role, player_level))

    tk.Label(add_window, text="Персонал команди").pack()

    staff_members = []  

    def add_staff_fields():
        frame = tk.Frame(add_window)
        frame.pack()
        
        tk.Label(frame, text="Ім'я").grid(row=0, column=0)
        staff_name = tk.Entry(frame)
        staff_name.grid(row=1, column=0)

        tk.Label(frame, text="Посада").grid(row=0, column=1)
        staff_position = tk.Entry(frame)
        staff_position.grid(row=1, column=1)
        
        staff_members.append((staff_name, staff_position))

    
    tk.Button(add_window, text="Додати ще персонал", command=add_staff_fields).pack(pady=5)

    # Тренувальна програма
    tk.Label(add_window, text="Тренувальна програма").pack()
    tk.Label(add_window, text="Назва програми").pack()
    entry_program_name = tk.Entry(add_window)
    entry_program_name.pack()

    tk.Label(add_window, text="Тривалість програми (днів)").pack()
    entry_program_duration = tk.Entry(add_window)
    entry_program_duration.pack()

    tk.Label(add_window, text="Напрямок").pack()
    entry_program_focus = tk.Entry(add_window)
    entry_program_focus.pack()

    def save_team():
        team_name = entry_team_name.get()
        coach_name = entry_coach_name.get()
        
        if not team_name or not coach_name:
            messagebox.showwarning("Помилка", "Введіть дані для команди та тренера.")
            return
        
        # Додаємо команду до БД
        c.execute("INSERT INTO teams (name) VALUES (?)", (team_name,))
        team_id = c.lastrowid

        # Додаємо гравців до БД
        for player_name, player_role, player_level in players:
            if player_name.get() and player_role.get() and player_level.get():  # Ensure level is also checked
                c.execute("INSERT INTO players (name, role, level, team_id) VALUES (?, ?, ?, ?)", 
                          (player_name.get(), player_role.get(), player_level.get(), team_id))

        # Додаємо персонал до бази даних
        for staff_name, staff_position in staff_members:
            if staff_name.get() and staff_position.get():  # Ensure both fields are filled
                c.execute("INSERT INTO staff (name, position, team_id) VALUES (?, ?, ?)", 
                          (staff_name.get(), staff_position.get(), team_id))
        
        program_name = entry_program_name.get()
        program_duration = entry_program_duration.get()
        program_focus = entry_program_focus.get()
        if program_name and program_duration and program_focus:
            try:
                program_duration = int(program_duration)  # Перетворюємо тривалість на число
                c.execute("INSERT INTO training_programs (name, duration, focus_area, team_id) VALUES (?, ?, ?, ?)",
                          (program_name, program_duration, program_focus, team_id))
                messagebox.showinfo("Успіх", "Тренувальна програма додана успішно!")
            except ValueError:
                messagebox.showwarning("Помилка", "Тривалість повинна бути числом.")

        conn.commit()
        messagebox.showinfo("Успіх", "Команда додана успішно!")
        add_window.destroy()
        root.deiconify() 

    tk.Button(add_window, text="Зберегти команду", command=save_team).pack(pady=5)
    tk.Button(add_window, text="Повернутися на головну", command=lambda: [add_window.destroy(), root.deiconify()]).pack(pady=5)

    add_staff_fields()  

# Додавання турнірів
def add_tournament_window(root):
    tournament_window = tk.Toplevel(root)
    tournament_window.title("Додати турнір")

    tk.Label(tournament_window, text="Назва турніру").pack()
    entry_tournament_name = tk.Entry(tournament_window)
    entry_tournament_name.pack()

    tk.Label(tournament_window, text="Місце проведення").pack()
    entry_location = tk.Entry(tournament_window)
    entry_location.pack()

    tk.Label(tournament_window, text="Початок турніру (YYYY-MM-DD)").pack()
    entry_start_date = tk.Entry(tournament_window)
    entry_start_date.pack()

    tk.Label(tournament_window, text="Кінець турніру (YYYY-MM-DD)").pack()
    entry_end_date = tk.Entry(tournament_window)
    entry_end_date.pack()

    tk.Label(tournament_window, text="Статус").pack()
    status_var = tk.StringVar(tournament_window)
    status_var.set("Скоро почнеться")  # Default value
    status_options = ["Скоро почнеться", "Триває", "Закінчився"]
    status_menu = tk.OptionMenu(tournament_window, status_var, *status_options)
    status_menu.pack()

    tk.Label(tournament_window, text="Призовий фонд").pack()
    entry_prize_fund = tk.Entry(tournament_window)
    entry_prize_fund.pack()

    def save_tournament():
        name = entry_tournament_name.get()
        location = entry_location.get()
        start_date = entry_start_date.get()
        end_date = entry_end_date.get()
        prize_fund = entry_prize_fund.get()
        status = status_var.get()

        if not name or not location or not start_date or not end_date or not prize_fund:
            messagebox.showwarning("Помилка", "Введіть усі дані для турніру.")
            return

        try:
            prize_fund = int(prize_fund)
        except ValueError:
            messagebox.showwarning("Помилка", "Призовий фонд має бути числом.")
            return

        # Збереження турнірів У БД
        c.execute("INSERT INTO tournaments (name, location, prize_fund, status, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?)", 
                  (name, location, prize_fund, status, start_date, end_date))
        conn.commit()
        messagebox.showinfo("Успіх", "Турнір доданий успішно!")
        tournament_window.destroy()
        root.deiconify()
    
    tk.Button(tournament_window, text="Зберегти турнір", command=save_tournament).pack(pady=5)
    tk.Button(tournament_window, text="Повернутися на головну", command=lambda: [tournament_window.destroy(), root.deiconify()]).pack(pady=5)

# Показ турнірів
def show_tournaments():
    tournament_window = tk.Toplevel()
    tournament_window.title("Ближчі турніри")

    tournament_window.geometry("900x900+500+100")
    
    tk.Button(tournament_window, text="Додати турнір", command=lambda: add_tournament_window(tournament_window)).pack(pady=5)

    c.execute("SELECT * FROM tournaments")
    tournaments = c.fetchall()

    for tournament in tournaments:
        frame = tk.Frame(tournament_window)
        frame.pack(pady=5)

        tk.Label(frame, text=f"{tournament[1]}, {tournament[2]}, Призовий фонд: {tournament[4]}, Статус: {tournament[5]}, Початок: {tournament[6]}, Кінець: {tournament[7]}").pack(side=tk.LEFT)
        tk.Button(frame, text="Видалити", command=lambda t_id=tournament[0]: delete_tournament(t_id, tournament_window)).pack(side=tk.RIGHT)

    
    tk.Button(tournament_window, text="Повернутися на головну", command=tournament_window.destroy).pack(pady=5)

# Видалення турнірів
def delete_tournament(t_id, tournament_window):
    c.execute("DELETE FROM tournaments WHERE id = ?", (t_id,))
    conn.commit()
    messagebox.showinfo("Успіх", "Турнір видалено!")
    tournament_window.destroy()
    show_tournaments()

# Показ команд
def show_teams():
    teams_window = tk.Toplevel()
    teams_window.title("Список команд та їх учасників")

    teams_window.geometry("700x700+500+100")
    
    c.execute("SELECT * FROM teams")
    teams = c.fetchall()
    
    for team in teams:
        frame = tk.Frame(teams_window)
        frame.pack(pady=5)
        
        # Відображення назви команди
        tk.Label(frame, text=f"Команда: {team[1]}").pack(side=tk.LEFT)

        # Кнопка видалення команди
        delete_button = tk.Button(frame, text="Видалити", command=lambda t_id=team[0]: delete_team(t_id, teams_window))
        delete_button.pack(side=tk.RIGHT)

        # Відображення гравців команди
        c.execute("SELECT * FROM players WHERE team_id = ?", (team[0],))
        players = c.fetchall()
        for player in players:
            tk.Label(frame, text=f"  Гравець: {player[1]}, Роль: {player[3]}").pack(side=tk.LEFT)

        # Відображення персоналу команди
        c.execute("SELECT * FROM staff WHERE team_id = ?", (team[0],))
        staff = c.fetchall()
        for staff_member in staff:
            tk.Label(frame, text=f"  Персонал: {staff_member[1]}, Позиція: {staff_member[2]}").pack(side=tk.LEFT)
        
    tk.Button(teams_window, text="Повернутися на головну", command=teams_window.destroy).pack(pady=5)

def delete_team(team_id, window):
    # Видалення гравців команди
    c.execute("DELETE FROM players WHERE team_id=?", (team_id,))
    # Видалення персоналу команди
    c.execute("DELETE FROM staff WHERE team_id=?", (team_id,))
    # Видалення команди
    c.execute("DELETE FROM teams WHERE id=?", (team_id,))
    conn.commit()

    messagebox.showinfo("Успіх", "Команду видалено успішно!")
    window.destroy()  # Закриваємо вікно зі списком команд
    show_teams()  # Поновлюємо список команд
 """
if __name__ == "__main__":
    """ main_window() """
    main_menu()
    conn.close()  # Закриття БД

