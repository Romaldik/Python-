from Team import Team

class Tournament:
    def __init__(self, name, prize_found):
        self.name = name
        self.prize_found = prize_found
        self.teams = []
    
    def add_team(self, team):
        self.teams.append(team)
        
    def start_tourment(self):
        print(f"Турнір {self.name} розпочався з призовим фондом {self.prize_found}")
        
    def end_tourment(self):
        print(f"Команда перемогла {Team.name} яка перемогла на турнірі {self.name} з призовим фондом {self.prize_found}")