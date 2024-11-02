from abc import ABC, abstractmethod

class TeamMember(ABC):
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    @abstractmethod  
    def train(self):
        pass
    
    @abstractmethod
    def analyze_perfomance(self):
        pass
    
    def __str__(self):
        return f"{self.name}, {self.age} років"
    
# Підклас абстрактного класу TeamMember 
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
    
# Підклас абстрактного класу TeamMember
class Coach(TeamMember):
    def __init__(self, name, age, style):
        super.__init__(name, age)
        self.style = style
        
    def train(self):
        print(f"Тренер {self.name} проводить тренування в стилі{self.style}")
        
    def analyze_perfomance(self):
        print(f"Тренер {self.name} аналізує результати команди.")

# Підклас абстрактного класу TeamMember
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