
__author__="vvladych"
__date__ ="$08.10.2014 06:04:16$"

from forecastmgmt.dao.db_connection import get_db_connection
from forecastmgmt.model.person import Person
import psycopg2.extras


class PersonDAO:
    
    def __init__(self):
        self.sql_select_dict={"get_all_persons":"SELECT sid, common_name, birth_date, birth_place, person_uuid FROM fc_person"}
        self.sql_insert_dict={"insert_person":"INSERT INTO fc_person(common_name, birth_date, birth_place) VALUES(%s,%s,%s) RETURNING sid"}
        
        
    def get_all_persons(self):
        personlist=[]
        cur = get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute(self.sql_select_dict["get_all_persons"])
        for person in cur.fetchall():
            personlist.append(Person(person.sid, person.common_name, person.birth_date, person.birth_place, person.person_uuid))
        cur.close()
        return personlist
    
    
    def insert(self, person):
        cur = get_db_connection().cursor()
        data=(person.common_name,person.birth_date,person.birth_place)
        cur.execute(self.sql_insert_dict["insert_person"],data)
        person.sid=cur.fetchone()[0]
    
        
    def get_uuid_from_sid(self,sid):
        pass
    
    
