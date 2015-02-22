
__author__="vvladych"
__date__ ="$10.02.2015 06:04:16$"

from forecastmgmt.dao.db_connection import get_db_connection
from forecastmgmt.model.person_name import PersonName
from forecastmgmt.dao.dao_utils import enum_retrieve_valid_values
import psycopg2.extras


class PersonNameDAO:
    
    def __init__(self):
        self.sql_select_dict={"get_person_name_role":"SELECT sid, name_role FROM fc_person_name WHERE fc_person_sid=%s"}
        self.sql_insert_dict={"insert_person_name":"INSERT INTO fc_person_name(fc_person_sid,name_role) VALUES(%s, %s) RETURNING sid"}
        
        
    def get_person_names(self, person_sid):
        personname_list=[]
        cur = get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute(self.sql_select_dict["get_person_name_role"] % person_sid)
        for personname in cur.fetchall():
            personname_list.append(PersonName(personname.sid, personname.name_role, person_sid))
        cur.close()
        return personname_list
    
    
    def insert_person_name(self, personname):
        cur = get_db_connection().cursor()
        print("name_role:%s" % personname.name_role)
        data=(personname.person_sid, personname.name_role,)
        cur.execute(self.sql_insert_dict["insert_person_name"], data)
        personname.sid=cur.fetchone()[0]
    
    
def get_person_name_roles():
    return enum_retrieve_valid_values("t_person_name_role")
    
