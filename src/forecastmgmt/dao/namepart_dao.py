
__author__="vvladych"
__date__ ="$08.10.2014 06:04:16$"

from forecastmgmt.dao.db_connection import get_db_connection
from forecastmgmt.model.namepart import Namepart
from forecastmgmt.dao.dao_utils import enum_retrieve_valid_values
import psycopg2.extras


class NamepartDAO:
    
    def __init__(self):
        self.sql_select_dict={"get_nameparts_for_person_sid":"SELECT sid, common_name, name_part_type, name_part_value FROM fc_person_name_part WHERE person_sid=%s"}
        self.sql_insert_dict={"insert_namepart":"INSERT INTO fc_person_name_part(name_part_type, name_part_value, person_sid) VALUES(%s, %s, %s) RETURNING sid"}
        
        
    def get_all_name_parts(self):
        namepart_list=[]
        cur = get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute(self.sql_select_dict["get_nameparts_for_person_sid"])
        for namepart in cur.fetchall():
            namepart_list.append(Namepart(namepart.sid, namepart.name_part_type, namepart.name_part_value, namepart.person_sid))
        cur.close()
        return namepart_list
    
    
    def insert_name_part(self, namepart):
        cur = get_db_connection().cursor()
        cur.execute(self.sql_insert_dict,(namepart.namepart_role, namepart.namepart_value, namepart.person_sid,))
        namepart.sid = cursor.fetchone()[0]
    
        
    def get_uuid_from_sid(self,sid):
        pass
    
    
    
def get_name_part_roles():
    return enum_retrieve_valid_values("t_person_name_part_role")
    
