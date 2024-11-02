import sqlite3

# SQLite database setup
def setup():
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
    return c, conn