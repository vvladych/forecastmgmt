
__author__="vvladych"
__date__ ="$09.10.2014 23:01:15$"


from forecastmgmt.dao.db_connection import get_db_connection
from forecastmgmt.dao.dao_utils import enum_retrieve_valid_values
import psycopg2.extras

from person_name import PersonName
from person_namepart import Namepart

class Person:
    
    sql_dict={"get_all_persons":"SELECT sid, common_name, birth_date, birth_place, person_uuid FROM fc_person", 
               "insert_person":"INSERT INTO fc_person(common_name, birth_date, birth_place) VALUES(%s,%s,%s) RETURNING sid",
               "delete_person":"DELETE FROM fc_person WHERE sid=%s",
               "load_person":"SELECT sid, common_name, birth_date, birth_place, person_uuid FROM fc_person WHERE sid=%s",
               "update_person":"UPDATE fc_person SET common_name=%s, birth_date=%s, birth_place=%s WHERE sid=%s",
               "get_person_name_role":"SELECT sid, name_role FROM fc_person_name WHERE fc_person_sid=%s",
               "get_nameparts_for_name_sid":"SELECT sid, name_part_role, name_part_value, person_name_sid FROM fc_person_name_part WHERE person_name_sid=%s"
               }
        
    def __init__(self, sid=None, common_name=None, birth_date=None, birth_place=None, person_uuid=None):
        self.sid=sid
        self.common_name=common_name
        self.birth_date=birth_date
        self.birth_place=birth_place
        self.person_uuid=person_uuid
        self.names=[]

            
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__==other.__dict__
        else:
            return False
        
    def __ne__(self, other):
        return not self==other

       
    def insert(self):
        cur = get_db_connection().cursor()
        data=(self.common_name,self.birth_date,self.birth_place)
        cur.execute(Person.sql_dict["insert_person"],data)
        self.sid=cur.fetchone()[0]
        cur.close()
        for name in self.names:
            name.person_sid=self.sid
            name.insert()
        get_db_connection().commit()
        
    
    def add_name(self, person_name_sid, person_name_role, person_sid, namepart_list):
        self.names.append(PersonName(person_name_sid, person_name_role, person_sid, namepart_list))
        
    def delete(self):
        cur = get_db_connection().cursor()
        data=(self.sid,)
        cur.execute(Person.sql_dict["delete_person"],data)
        cur.close()
        get_db_connection().commit()
        
    def load(self):
        cur=get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        data=(self.sid,)
        cur.execute(Person.sql_dict["load_person"],data)
        for p in cur.fetchall():
            self.sid=p.sid
            self.common_name=p.common_name
            self.birth_date=p.birth_date
            self.birth_place=p.birth_place
            self.person_uuid=p.person_uuid
            self._load_person_names()
        cur.close()   
        
    def _load_person_names(self):
        self.names=[]
        cur = get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute(self.sql_dict["get_person_name_role"] % self.sid)
        for personname in cur.fetchall():
            self.names.append(PersonName(personname.sid, personname.name_role, self.sid, self._load_person_name_parts(personname.sid)))
        cur.close()
                
    def _load_person_name_parts(self, personname_sid):
        namepart_list=[]
        cur = get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        data=(personname_sid,)
        cur.execute(self.sql_dict["get_nameparts_for_name_sid"], data)
        for namepart in cur.fetchall():
            namepart_list.append(Namepart(namepart.sid, namepart.name_part_role, namepart.name_part_value, namepart.person_name_sid))
        cur.close()
        return namepart_list        
        
    def update(self, other):
        cur=get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        data=(other.common_name, other.birth_date, other.birth_place, self.sid)
        cur.execute(Person.sql_dict["update_person"],data)
        cur.close()
        
        # update person_names
        # delete outdated person_names
        for person_name in self.names:
            if person_name not in other.names:
                person_name.delete()
                
        for person_name in other.names:
            if person_name not in self.names:
                person_name.insert()
            
        get_db_connection().commit()
        


def get_all_persons():
    personlist=[]
    cur = get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cur.execute(Person.sql_dict["get_all_persons"])
    for person in cur.fetchall():
        personlist.append(Person(person.sid, person.common_name, person.birth_date, person.birth_place, person.person_uuid))
    cur.close()
    return personlist

