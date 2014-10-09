
__author__="vvladych"
__date__ ="$08.10.2014 06:04:16$"

from db_connection import get_db_connection


class PersonDAO:
    
    def __init__(self):
        self.personlist=[]
        
    def get_all_persons(self):
        cur = db_connection.get_db_connection().cursor()
        cur.execute("SELECT sid, common_name, person_uuid FROM person")
        persons = cur.fetchall()
        cur.close()
    