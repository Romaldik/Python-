from src.DataBase.db_utils import get_table_list 

def main():
    tables = get_table_list()
    if tables:
        print("Tables in the database:")
        for table in tables:
            print(table)
    else:
        print("No tables found or error in connection.")

if __name__ == "__main__":
    main()