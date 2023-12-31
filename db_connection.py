import sys
import psycopg2
from os import environ as env
from dotenv import load_dotenv

load_dotenv()
connection = cursor = db = None

def connect():
    global connection, cursor, db
    try:
        connection = psycopg2.connect(env['DATABASE_URI'])
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
