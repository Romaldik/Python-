from . import create_connection

class dbUtils:
    def __init__(self) -> None:
        self.connection = create_connection()

    def get_table_list(self,):
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
                    tables = cursor.fetchall()
                    table_names = [table[0] for table in tables]
                    return table_names
            except Exception as e:
                print(f"Error fetching table list: {e}")
            finally:
                self.connection.close()
        return []
    