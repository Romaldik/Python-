from TeamMember import TeamMember

class Staff(TeamMember):
    def __init__(self, name, age, position):
        super().__init__(name, age)
        self.position = position
    
    def train(self):
        print(f"{self.position} {self.name} надає підтримку команді.")

    def analyze_perfomance(self):
        print(f"{self.position} {self.name} проводить аналіз виступів команди.")

    def __str__(self):
        return f"{self.position} {self.name}, {self.age} років"
