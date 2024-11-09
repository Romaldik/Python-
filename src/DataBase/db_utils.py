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