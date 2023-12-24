import sys
import psycopg2
from os import environ as env
# from sqlalchemy import create_engine

con = cur = db = None

# engine = create_engine(env["DATABASE_URI"])

def connect():
    global con, cur, db
    try:
        con = psycopg2.connect(
            host=env["HOST"],
            port=env["DB_PORT"],
            dbname=env["DATABASE"],
            user=env["USER"],
            password=env["PASSWORD"]
        )
        cur = con.cursor()
        db = cur.execute
    except psycopg2.DatabaseError as ex:
        if con:
            con.rollback()
        print(ex)
        sys.exit()


def get_db():
    if not (con and cur and db):
        connect()
    return (con, cur, db)
