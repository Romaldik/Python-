import unittest
import psycopg2
from psycopg2 import sql

class TestDatabaseOperations(unittest.TestCase):
    
    def setUp(self):
        # Connect to the database
        self.conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='esportsmanager',
            user='alex',
            password='ayana1212'
        )
        self.cursor = self.conn.cursor()

    def tearDown(self):
        # Cleanup: Close connection after each test
        self.cursor.close()
        self.conn.close()

    def test_insert_team(self):
        # Test inserting a team
        self.cursor.execute("""
            INSERT INTO TrainingProgram (name, duration) VALUES ('Pro Training', '1 year') RETURNING id;
        """)
        training_program_id = self.cursor.fetchone()[0]

        self.cursor.execute("""
            INSERT INTO Team (name, location, training_program_id, period_of_sponsorship) 
            VALUES ('G2', 'Berlin', %s, '2 years') RETURNING id;
        """, (training_program_id,))
        team_id = self.cursor.fetchone()[0]
        
        # Assert team was inserted correctly
        self.cursor.execute("SELECT * FROM Team WHERE id = %s;", (team_id,))
        team = self.cursor.fetchone()
        self.assertIsNotNone(team)
        self.assertEqual(team[1], 'G2')  # Check team name is 'G2'

    def test_insert_player(self):
        # Test inserting a player linked to a team
        self.cursor.execute("""
            INSERT INTO TrainingProgram (name, duration) VALUES ('Pro Training', '1 year') RETURNING id;
        """)
        training_program_id = self.cursor.fetchone()[0]

        self.cursor.execute("""
            INSERT INTO Team (name, location, training_program_id, period_of_sponsorship) 
            VALUES ('G2', 'Berlin', %s, '2 years') RETURNING id;
        """, (training_program_id,))
        team_id = self.cursor.fetchone()[0]

        self.cursor.execute("""
            INSERT INTO Player (FullName, Nickname, age, Role, team_id) 
            VALUES ('John Doe', 'jDoe', 25, 'Rifler', %s) RETURNING id;
        """, (team_id,))
        player_id = self.cursor.fetchone()[0]

        # Assert player was inserted correctly
        self.cursor.execute("SELECT * FROM Player WHERE id = %s;", (player_id,))
        player = self.cursor.fetchone()
        self.assertIsNotNone(player)
        self.assertEqual(player[1], 'John Doe')  # Check player's full name

    def test_foreign_key_constraint(self):
        # Test that ON DELETE SET NULL works for Player when Team is deleted
        self.cursor.execute("""
            INSERT INTO TrainingProgram (name, duration) VALUES ('Pro Training', '1 year') RETURNING id;
        """)
        training_program_id = self.cursor.fetchone()[0]

        self.cursor.execute("""
            INSERT INTO Team (name, location, training_program_id, period_of_sponsorship) 
            VALUES ('G2', 'Berlin', %s, '2 years') RETURNING id;
        """, (training_program_id,))
        team_id = self.cursor.fetchone()[0]

        self.cursor.execute("""
            INSERT INTO Player (FullName, Nickname, age, Role, team_id) 
            VALUES ('John Doe', 'jDoe', 25, 'Rifler', %s) RETURNING id;
        """, (team_id,))
        player_id = self.cursor.fetchone()[0]

        # Delete the team
        self.cursor.execute("DELETE FROM Team WHERE id = %s;", (team_id,))

        # Assert that the player's team_id is now NULL
        self.cursor.execute("SELECT team_id FROM Player WHERE id = %s;", (player_id,))
        team_id_after_deletion = self.cursor.fetchone()[0]
        self.assertIsNone(team_id_after_deletion)

    def test_team_sponsor_relationship(self):
        # Test inserting team-sponsor relationship
        self.cursor.execute("""
            INSERT INTO TrainingProgram (name, duration) VALUES ('Pro Training', '1 year') RETURNING id;
        """)
        training_program_id = self.cursor.fetchone()[0]


        self.cursor.execute("""
            INSERT INTO Team (name, location, training_program_id, period_of_sponsorship) 
            VALUES ('G2', 'Berlin', %s, '2 years') RETURNING id;
        """, (training_program_id,))
        team_id = self.cursor.fetchone()[0]

        self.cursor.execute("INSERT INTO Sponsor (name) VALUES ('Monster Energy') RETURNING id;")
        sponsor_id = self.cursor.fetchone()[0]

        # Create team-sponsor relationship
        self.cursor.execute("""
            INSERT INTO Team_Sponsor (team_id, sponsor_id) 
            VALUES (%s, %s);
        """, (team_id, sponsor_id))

        # Assert that the relationship exists
        self.cursor.execute("""
            SELECT * FROM Team_Sponsor WHERE team_id = %s AND sponsor_id = %s;
        """, (team_id, sponsor_id))
        relationship = self.cursor.fetchone()
        self.assertIsNotNone(relationship)

if __name__ == '__main__':
    unittest.main()
