from TeamMember import TeamMember 
# підклас абстрактного класу TeamMember 
class Player(TeamMember):
    def __init__(self, name, age, skills, role):
        super().__init__(name, age)
        self.skills = skills
        self.role = role
        
    def train(self):
        print(f"{self.name} тренується для покращення навичок.")
        
    def analyze_perfomence(self):
        print(f"Аналіз виступу гравця {self.name}. Його навички: {self.skills}")
        
    def __str__(self):
        return f"{self.name} ({self.role}), навички {self.skills}"