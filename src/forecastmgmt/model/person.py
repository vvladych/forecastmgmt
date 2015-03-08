
__author__="vvladych"
__date__ ="$09.10.2014 23:01:15$"


from forecastmgmt.dao.db_connection import get_db_connection
from forecastmgmt.dao.dao_utils import enum_retrieve_valid_values
import psycopg2.extras

class Person:
    
    sql_dict={"get_all_persons":"SELECT sid, common_name, birth_date, birth_place, person_uuid FROM fc_person", 
               "insert_person":"INSERT INTO fc_person(common_name, birth_date, birth_place) VALUES(%s,%s,%s) RETURNING sid",
               "delete_person":"DELETE FROM fc_person WHERE sid=%s",
               "load_person":"SELECT sid, common_name, birth_date, birth_place, person_uuid FROM fc_person WHERE sid=%s"
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
            print("self: %s " % self.__dict__)
            print("other: %s " % other.__dict__)
            
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
        
    
    def add_name(self, name):
        self.names.append(name)
        
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
            self.names = get_person_names(self.sid)
        cur.close()   


def get_all_persons():
    personlist=[]
    cur = get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cur.execute(Person.sql_dict["get_all_persons"])
    for person in cur.fetchall():
        personlist.append(Person(person.sid, person.common_name, person.birth_date, person.birth_place, person.person_uuid))
    cur.close()
    return personlist

        
class PersonName:
    sql_dict={"get_person_name_role":"SELECT sid, name_role FROM fc_person_name WHERE fc_person_sid=%s",
              "insert_person_name":"INSERT INTO fc_person_name(fc_person_sid,name_role) VALUES(%s, %s) RETURNING sid"
              }    
                
    def __init__(self, sid=None, name_role=None, person_sid=None, nameparts=[]):
        self.sid=sid
        self.name_role=name_role
        self.person_sid=person_sid
        self.nameparts=nameparts


            
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            print("name self: %s " % self.__dict__)
            print("name other: %s " % other.__dict__)
            return self.__dict__==other.__dict__
        else:
            return False

    
    def insert(self):
        cur = get_db_connection().cursor()
        data=(self.person_sid, self.name_role,)
        cur.execute(PersonName.sql_dict["insert_person_name"], data)
        self.sid=cur.fetchone()[0]
        for namepart in self.nameparts:
            namepart.person_name_sid=self.sid
            namepart.insert()
        
    def add_namepart(self, namepart):
        self.nameparts.append(namepart)
                         
    
def get_person_names(person_sid):
    personname_list=[]
    cur = get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cur.execute(PersonName.sql_dict["get_person_name_role"] % person_sid)
    for personname in cur.fetchall():
        personname_list.append(PersonName(personname.sid, personname.name_role, person_sid, get_all_name_parts(personname.sid)))
    cur.close()
    return personname_list

def get_person_name_roles():
    return enum_retrieve_valid_values("t_person_name_role")



class Namepart:
    
    sql_dict={"get_nameparts_for_name_sid":"SELECT sid, name_part_role, name_part_value, person_name_sid FROM fc_person_name_part WHERE person_name_sid=%s",
                "insert_namepart":"INSERT INTO fc_person_name_part(name_part_role, name_part_value, person_name_sid) VALUES(%s, %s, %s) RETURNING sid"}
        
    def __init__(self, sid=None, namepart_role=None, namepart_value=None, person_name_sid=None):
        self.sid=sid
        self.namepart_role=namepart_role
        self.namepart_value=namepart_value
        self.person_name_sid=person_name_sid
            
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            print("namepart self: %s " % self.__dict__)
            print("namepart other: %s " % other.__dict__)

            return self.__dict__==other.__dict__
        else:
            return False

    def insert(self):
        cur = get_db_connection().cursor()
        cur.execute(Namepart.sql_dict["insert_namepart"],(self.namepart_role, self.namepart_value, self.person_name_sid,))
        self.sid = cur.fetchone()[0]
        cur.close()
        

def get_all_name_parts(name_sid):
    namepart_list=[]
    cur = get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    data=(name_sid,)
    cur.execute(Namepart.sql_dict["get_nameparts_for_name_sid"], data)
    for namepart in cur.fetchall():
        namepart_list.append(Namepart(namepart.sid, namepart.name_part_role, namepart.name_part_value, namepart.person_name_sid))
    cur.close()
    return namepart_list

def get_name_part_roles():
    return enum_retrieve_valid_values("t_person_name_part_role")
    
