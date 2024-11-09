import psycopg2
from psycopg2 import OperationalError

def create_connection():
    try:
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='esportsmanager',
            user='alex',
            password='ayana1212'
        )
        return conn
    except OperationalError as e:
        return None