
__author__="vvladych"
__date__ ="$08.10.2014 06:22:15$"

import psycopg2

__all__ = ['get_db_connection']

class Error(Exception):
    pass

class InvalidMethodException(Error):
    pass

dbInstance=None

def get_db_connection():
    global dbInstance
    if dbInstance is None:
        dbInstance=psycopg2.connect("dbname=forecast user=vklein password=vklein34")
    return dbInstance


if __name__=="__main__":
    get_db_connection()
