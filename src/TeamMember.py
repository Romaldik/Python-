from abc import ABC, abstractmethod
# абстрактний клас TeamMember
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
    
    
