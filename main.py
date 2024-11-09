from src.mypackage.TeamMember import Player

def main():
    a = Player("Aleksi", 'a', 21, 'Rdf', 'Navi')
    #a.add_people()
    #a.delete_people()
    print(a.__str__())

if __name__ == "__main__":
    main()