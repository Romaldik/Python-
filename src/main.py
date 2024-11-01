import tkinter as tk
from tkinter import messagebox
import sqlite3
from Team import Team
from Player import Player
from Coach import Coach
from Staff import Staff
from Sponsor import Sponsor

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

conn.commit()

# Графічний інтерфес
def main_window():
    root = tk.Tk()
    root.title("Кіберспортивний менеджер")
    
    def open_add_team_window():
        root.withdraw()  # Hide main window
        add_team_window(root)
    
    def open_add_tournament_window():
        root.withdraw()
        add_tournament_window(root)

    tk.Label(root, text="Головне меню", font=("Arial", 16)).pack(pady=10)
    tk.Button(root, text="Додати команду", command=open_add_team_window).pack(pady=5)
    tk.Button(root, text="Ближчі турніри", command=show_tournaments).pack(pady=5)
    tk.Button(root, text="Список команд та їх гравців", command=show_teams).pack(pady=5)
    tk.Button(root, text="Вихід", command=root.quit).pack(pady=5)

    root.mainloop()

# Додавання команли
def add_team_window(root):
    add_window = tk.Toplevel(root)
    add_window.title("Додати команду")
    
    tk.Label(add_window, text="Назва команди").pack()
    entry_team_name = tk.Entry(add_window)
    entry_team_name.pack()
    
    tk.Label(add_window, text="Тренер").pack()
    entry_coach_name = tk.Entry(add_window)
    entry_coach_name.pack()
    
    players = []
    tk.Label(add_window, text="Учасники команди").pack()

    # Create headers for the player details
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

    staff_members = []  # List to hold staff input fields

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

    # Button to add more staff fields
    tk.Button(add_window, text="Додати ще персонал", command=add_staff_fields).pack(pady=5)

    def save_team():
        team_name = entry_team_name.get()
        coach_name = entry_coach_name.get()
        
        if not team_name or not coach_name:
            messagebox.showwarning("Помилка", "Введіть дані для команди та тренера.")
            return
        
        # Додаємо команду до бази даних
        c.execute("INSERT INTO teams (name) VALUES (?)", (team_name,))
        team_id = c.lastrowid

        # Додаємо гравців до бази даних
        for player_name, player_role, player_level in players:
            if player_name.get() and player_role.get() and player_level.get():  # Ensure level is also checked
                c.execute("INSERT INTO players (name, role, level, team_id) VALUES (?, ?, ?, ?)", 
                          (player_name.get(), player_role.get(), player_level.get(), team_id))

        # Додаємо персонал до бази даних
        for staff_name, staff_position in staff_members:
            if staff_name.get() and staff_position.get():  # Ensure both fields are filled
                c.execute("INSERT INTO staff (name, position, team_id) VALUES (?, ?, ?)", 
                          (staff_name.get(), staff_position.get(), team_id))

        conn.commit()
        messagebox.showinfo("Успіх", "Команда додана успішно!")
        add_window.destroy()
        root.deiconify()  # Повернутись до головного вікна

    tk.Button(add_window, text="Зберегти команду", command=save_team).pack(pady=5)
    tk.Button(add_window, text="Повернутися на головну", command=lambda: [add_window.destroy(), root.deiconify()]).pack(pady=5)

    # Initial call to create staff fields
    add_staff_fields()  # Start with one staff entry by default

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

    # Додавання турнірів
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

    c.execute("SELECT * FROM teams")
    teams = c.fetchall()
    
    for team in teams:
        tk.Label(teams_window, text=f"Команда: {team[1]}").pack(pady=5)

        c.execute("SELECT * FROM players WHERE team_id = ?", (team[0],))
        players = c.fetchall()
        for player in players:
            tk.Label(teams_window, text=f"  Гравець: {player[1]}, Роль: {player[3]}").pack(pady=2)

        c.execute("SELECT * FROM staff WHERE team_id = ?", (team[0],))
        staff = c.fetchall()
        for staff_member in staff:
            tk.Label(teams_window, text=f"  Персонал: {staff_member[1]}, Позиція: {staff_member[2]}").pack(pady=2)

    tk.Button(teams_window, text="Повернутися на головну", command=teams_window.destroy).pack(pady=5)

if __name__ == "__main__":
    main_window()
    conn.close()  # Закриття БД

