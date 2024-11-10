from .TeamMember import Player, Coach, Staff

class Team:
    def __init__(self, name, location, trining_prog, period_of_sponsorship):
        self.name = name
        self.location = location
        self.trining_prog = trining_prog
        self.period_of_sponsorship = period_of_sponsorship
        
    def create_team(self):
        pass
    
    def delete_team(self):
        pass

    def change_team_player(self):
        pass

    def change_team_coach(self):
        pass

    def change_team_staff(self):
        pass

    def add_player(self):
        pass

    def add_coach(self):
        pass

    def add_staff(self):
        pass

    def add_sponsor(self):
        pass  
    
    def __str__(self):
        return f"Команда {self.name} має {len(self.members)} членів і {len(self.sponsors)} спонсорів."
