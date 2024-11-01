from Team import Team
# клас Sponsor спосор 
class Sponsor:
    def __init__(self, name, offer):
        self.name = name
        self.offer = offer
    
    def negotiate(self, team):
        print(f"Спонсор {self.name} пропонує підтримку команді {Team.name}")
        