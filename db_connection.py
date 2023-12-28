import sys
import psycopg2
from os import environ as env
connection = cursor = db = None

def connect():
    global connection, cursor, db
    try:
        connection = psycopg2.connect(
            host="db.uksjmnsviwcdehlinbcp.supabase.co",
            port="5432",
            dbname="postgres",
            user="postgres",
            password="Ts9_Gzx?dU8ddQ+"
        )
        cursor = connection.cursor()
        db = cursor.execute
        print("Database connected")
    except psycopg2.DatabaseError as ex:
        if connection:
            connection.rollback()
        print(ex)
        print("Database connection error")
        sys.exit()


def get_db():
    if not (connection and cursor and db):
        connect()
    return (connection, cursor, db)
