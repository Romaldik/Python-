from TeamMember import TeamMember
# підклас абстрактного класу TeamMember Тренер

class Coach(TeamMember):
    def __init__(self, name, age, style):
        super.__init__(name, age)
        self.style = style
        
    def train(self):
        print(f"Тренер {self.name} проводить тренування в стилі{self.style}")
        
    def analyze_perfomance(self):
        print(f"Тренер {self.name} аналізує результати команди.")