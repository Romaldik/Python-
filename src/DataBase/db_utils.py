from . import create_connection

def get_table_list():
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
                tables = cursor.fetchall()
                table_names = [table[0] for table in tables]
                return table_names
        except Exception as e:
            print(f"Error fetching table list: {e}")
        finally:
            connection.close()
    return []

def select_query(query, value):    
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, value)
                return cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            connection.close()
    return None

def execute_query(query, value):    
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, value)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            connection.close()


class dbUtils:
    def __init__(self, table_name, data) -> None:
        self.table_name = table_name
        self.data = data

    def add_data(self,):
        conn = create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(f'SELECT * FROM {self.table_name} LIMIT 0;')
                    column_names = [desc[0] for desc in cursor.description]

                    columns = ', '.join(column_names)
                    placeholders = ', '.join(['%s'] * len(column_names))
                    insert_query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders});"

                    cursor.execute(insert_query, self.data)
                    conn.commit()
            except Exception as e:
                print(f"Error: {e}")
            finally:
                conn.close()