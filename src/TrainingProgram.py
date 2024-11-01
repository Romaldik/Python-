from __init__ import Player

class TrainingProgram:
    def __init__(self, name, duration, focus_area):
        self.name = name
        self.duration = duration  
        self.focus_area = focus_area  

    def start_program(self, team):
        print(f"Розпочато тренування '{self.name}' тривалістю {self.duration} днів.")
        for member in team.members:
            if isinstance(member, Player):
                print(f"Гравець {member.name} тренується у напрямку {self.focus_area}.")

    def __str__(self):
        return f"Тренувальна програма '{self.name}' з фокусом на {self.focus_area}"
