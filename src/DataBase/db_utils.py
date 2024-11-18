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
    def __init__(self) -> None:
        pass

    def get_data(param, table_name, name):    
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    get_query = f'SELECT {param} FROM {table_name} WHERE name = %s;'
                    cursor.execute(get_query, (name,))
                    return cursor.fetchone()
            except Exception as e:
                print(f"Error: {e}")
            finally:
                connection.close()
        return None
    
    def add_data(table_name, data):
        conn = create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(f'SELECT * FROM {table_name} LIMIT 0;')
                    column_names = [desc[0] for desc in cursor.description]

                    columns = ', '.join(column_names[1:])
                    placeholders = ', '.join(['%s'] * len(column_names[1:]))
                    
                    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"

                    cursor.execute(insert_query, data)
                    conn.commit()
            except Exception as e:
                print(f"Error: {e}")
            finally:
                conn.close()

    def delete_data(table_name, id):
        conn = create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    delete_query = f"DELETE FROM {table_name} WHERE id = %s"

                    cursor.execute(delete_query, id)
                    conn.commit()
            except Exception as e:
                print(f"Error: {e}")
            finally:
                conn.close()

    def update_data(table_name, column_name, value_1, id, value_2):
        conn = create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    update_query = f"UPDATE {table_name} SET {column_name} = {value_1} WHERE {id} = {value_2};"

                    cursor.execute(update_query)
                    conn.commit()
            except Exception as e:
                print(f"Error: {e}")
            finally:
                conn.close()

    def show_data(table_name, table1, table2, id_name):    
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    query = f"SELECT p.*, COALESCE(t.name, 'None') AS {table_name} FROM {table1} p LEFT JOIN {table2} t ON p.{id_name} = t.id;"
                    cursor.execute(query)
                    
                    columns = [desc[0] for desc in cursor.description] 
                    filtered_columns = [col for col in columns if 'id' not in col.lower()]
                    results = [
                        {col: value for col, value in zip(columns, row) if col in filtered_columns}
                        for row in cursor.fetchall()
                    ]
                    return results
            except Exception as e:
                    print(f"Error: {e}")
            finally:
                connection.close()
        return None
    
    def show_table(table_name):
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    query = f"SELECT * FROM {table_name};"
                    cursor.execute(query)
                    
                    columns = [desc[0] for desc in cursor.description] 
                    filtered_columns = [col for col in columns if 'id' not in col.lower()]
                    results = [
                        {col: value for col, value in zip(columns, row) if col in filtered_columns}
                        for row in cursor.fetchall()
                    ]
                    return results
            except Exception as e:
                    print(f"Error: {e}")
            finally:
                connection.close()
        return None