from src.mypackage.TeamMember import Player
from src.mypackage.Team import Team

def main():
    #a = Player("Aleksi", 'a', 21, 'Rdf', 'Navi')
    #a.add_people()
    #a.delete_people()
    #print(a.__str__())
    a = Team('Navi', 'Europe', '1day', '12 days')
    #a.create_team()
    a.delete_team('Navi')


if __name__ == "__main__":
    main()