import tkinter as tk
from tkinter import messagebox
from .DataBase import setup

class EsportsManagerWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.c, self.conn  = setup()
        print(self.c, self.conn)
        self.root.title("Кіберспортивний менеджер")
        self.root.geometry("900x900+500+100")
        self.main_window()
    
    def close_connection(self):
        self.conn.close()

    def main_window(self):
        tk.Label(self.root, text="Головне меню", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Додати команду", command=self.open_add_team_window).pack(pady=5)
        tk.Button(self.root, text="Ближчі турніри", command=self.show_tournaments).pack(pady=5)
        tk.Button(self.root, text="Список команд та їх гравців", command=self.show_teams).pack(pady=5)
        tk.Button(self.root, text="Вихід", command=self.root.quit).pack(pady=5)

    def open_add_team_window(self):
        self.root.withdraw()
        add_window = tk.Toplevel(self.root)
        add_window.title("Додати команду")
        add_window.geometry("800x800+500+100")
        
        self.add_team_fields(add_window)
        tk.Button(add_window, text="Зберегти команду", command=lambda: self.save_team(add_window)).pack(pady=5)
        tk.Button(add_window, text="Повернутися на головну", command=lambda: [add_window.destroy(), self.root.deiconify()]).pack(pady=5)

    def add_team_fields(self, add_window):
        tk.Label(add_window, text="Назва команди").pack()
        self.entry_team_name = tk.Entry(add_window)
        self.entry_team_name.pack()
        
        tk.Label(add_window, text="Тренер").pack()
        self.entry_coach_name = tk.Entry(add_window)
        self.entry_coach_name.pack()

        self.players = []
        tk.Label(add_window, text="Учасники команди").pack()
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
            self.players.append((player_name, player_role, player_level))

        self.staff_members = []
        tk.Button(add_window, text="Додати ще персонал", command=self.add_staff_fields).pack(pady=5)

        self.training_program_fields(add_window)

    def add_staff_fields(self):
        frame = tk.Frame(self.root)
        frame.pack()
        tk.Label(frame, text="Ім'я").grid(row=0, column=0)
        staff_name = tk.Entry(frame)
        staff_name.grid(row=1, column=0)

        tk.Label(frame, text="Посада").grid(row=0, column=1)
        staff_position = tk.Entry(frame)
        staff_position.grid(row=1, column=1)
        
        self.staff_members.append((staff_name, staff_position))

    def training_program_fields(self, add_window):
        tk.Label(add_window, text="Тренувальна програма").pack()
        tk.Label(add_window, text="Назва програми").pack()
        self.entry_program_name = tk.Entry(add_window)
        self.entry_program_name.pack()

        tk.Label(add_window, text="Тривалість програми (днів)").pack()
        self.entry_program_duration = tk.Entry(add_window)
        self.entry_program_duration.pack()

        tk.Label(add_window, text="Напрямок").pack()
        self.entry_program_focus = tk.Entry(add_window)
        self.entry_program_focus.pack()

    def save_team(self, add_window):
        team_name = self.entry_team_name.get()
        coach_name = self.entry_coach_name.get()
        if not team_name or not coach_name:
            messagebox.showwarning("Помилка", "Введіть дані для команди та тренера.")
            return
        
        # Збереження команди та гравців
        self.c.execute("INSERT INTO teams (name) VALUES (?)", (team_name,))
        team_id = self.c.lastrowid
        for player_name, player_role, player_level in self.players:
            if player_name.get() and player_role.get() and player_level.get():
                self.c.execute("INSERT INTO players (name, role, level, team_id) VALUES (?, ?, ?, ?)", 
                              (player_name.get(), player_role.get(), player_level.get(), team_id))
        
        for staff_name, staff_position in self.staff_members:
            if staff_name.get() and staff_position.get():
                self.c.execute("INSERT INTO staff (name, position, team_id) VALUES (?, ?, ?)", 
                              (staff_name.get(), staff_position.get(), team_id))
        
        program_name = self.entry_program_name.get()
        program_duration = self.entry_program_duration.get()
        program_focus = self.entry_program_focus.get()
        if program_name and program_duration and program_focus:
            try:
                program_duration = int(program_duration)
                self.c.execute("INSERT INTO training_programs (name, duration, focus_area, team_id) VALUES (?, ?, ?, ?)",
                              (program_name, program_duration, program_focus, team_id))
                messagebox.showinfo("Успіх", "Тренувальна програма додана успішно!")
            except ValueError:
                messagebox.showwarning("Помилка", "Тривалість повинна бути числом.")
        
        self.conn.commit()
        messagebox.showinfo("Успіх", "Команда додана успішно!")
        add_window.destroy()
        self.root.deiconify()

    def show_tournaments(self):
        tournament_window = tk.Toplevel(self.root)
        tournament_window.title("Ближчі турніри")
        tk.Button(tournament_window, text="Додати турнір", command=lambda: self.open_add_tournament_window(tournament_window)).pack(pady=5)
        self.c.execute("SELECT * FROM tournaments")
        tournaments = self.c.fetchall()
        for tournament in tournaments:
            frame = tk.Frame(tournament_window)
            frame.pack(pady=5)
            tk.Label(frame, text=f"{tournament[1]}, {tournament[2]}, Призовий фонд: {tournament[4]}, Статус: {tournament[5]}, Початок: {tournament[6]}, Кінець: {tournament[7]}").pack(side=tk.LEFT)
            tk.Button(frame, text="Видалити", command=lambda t_id=tournament[0]: self.delete_tournament(t_id, tournament_window)).pack(side=tk.RIGHT)
        tk.Button(tournament_window, text="Повернутися на головну", command=tournament_window.destroy).pack(pady=5)

    def open_add_tournament_window(self, parent):
        # Метод відкриття вікна додавання турніру
        pass
    
    def delete_tournament(self, t_id, tournament_window):
        self.c.execute("DELETE FROM tournaments WHERE id = ?", (t_id,))
        self.conn.commit()
        messagebox.showinfo("Успіх", "Турнір видалено!")
        tournament_window.destroy()
        self.show_tournaments()

    def show_teams(self):
        teams_window = tk.Toplevel(self.root)
        teams_window.title("Список команд та їх учасників")
        self.c.execute("SELECT * FROM teams")
        teams = self.c.fetchall()
        for team in teams:
            frame = tk.Frame(teams_window)
            frame.pack(pady=5)
            tk.Label(frame, text=f"Команда: {team[1]}").pack(side=tk.LEFT)
            tk.Button(frame, text="Видалити", command=lambda t_id=team[0]: self.delete_team(t_id, teams_window)).pack(side=tk.RIGHT)
            # Відображення гравців команди
            self.c.execute("SELECT * FROM players WHERE team_id = ?", (team[0],))
            players = self.c.fetchall()
            for player in players:
                tk.Label(frame, text=f"  Гравець: {player[1]}, Роль: {player[3]}").pack(side=tk.LEFT)
            # Відображення персоналу
            self.c.execute("SELECT * FROM staff WHERE team_id = ?", (team[0],))
            staff = self.c.fetchall()
            for staff_member in staff:
                tk.Label(frame, text=f"  Персонал: {staff_member[1]}, Позиція: {staff_member[2]}").pack(side=tk.LEFT)
        tk.Button(teams_window, text="Повернутися на головну", command=teams_window.destroy).pack(pady=5)

    def delete_team(self, team_id, window):
        self.c.execute("DELETE FROM players WHERE team_id=?", (team_id,))
        self.c.execute("DELETE FROM staff WHERE team_id=?", (team_id,))
        self.c.execute("DELETE FROM teams WHERE id=?", (team_id,))
        self.conn.commit()
        messagebox.showinfo("Успіх", "Команду видалено успішно!")
        window.destroy()
        self.show_teams()