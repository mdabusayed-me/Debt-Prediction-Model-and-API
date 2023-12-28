import sys
import psycopg2
from os import environ as env


connection = cursor = db = None

def connect():
    global connection, cursor, db
    try:
        connection = psycopg2.connect("postgresql://postgres:Ts9GzxdU8ddQ@db.uksjmnsviwcdehlinbcp.supabase.co:5432/postgres")
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
