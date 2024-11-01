from TeamMember import TeamMember
from Player import Player
from Coach import Coach
from Staff import Staff
class Team:
    def __init__(self, name):
        self.name = name
        self.members = []
        self.sponsors = []
        self.training_programs = []
    
    def recruit_member(self, member):
        if isinstance(member, (Player, Coach, Staff)):
            self.members.append(member)
            print(f"{member} додано до команди.")
        else:
            raise ValueError("Член команди повинен бути гравцем, тренером або персоналом.")

    def organize_practice(self, training_program):
        if training_program not in self.training_programs:
            self.training_programs.append(training_program)
        training_program.start_program(self)
        print(f"Організовано тренування: {training_program}")

    def participate_tournament(self, tournament):
        tournament.add_team(self)
        print(f"Команда {self.name} бере участь у турнірі '{tournament.name}'.")

    def negotiate_sponsorship(self, sponsor):
        self.sponsors.append(sponsor)
        sponsor.negotiate(self)
        print(f"Укладено спонсорську угоду з {sponsor.name}")

    def analyze_performence(self):
        for member in self.members:
            member.analyze_perfomence()

    def list_members(self):
        return [str(member) for member in self.members]
    
    def __str__(self):
        return f"Команда {self.name} має {len(self.members)} членів і {len(self.sponsors)} спонсорів."
