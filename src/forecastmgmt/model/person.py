
__author__="vvladych"
__date__ ="$09.10.2014 23:01:15$"


from src.forecastmgmt.dao.db_connection import get_db_connection
import psycopg2.extras

from src.forecastmgmt.model.MDO import MDO

from src.forecastmgmt.model.person_name import PersonName

class Person(MDO):
    
    sql_dict={"get_all":"SELECT sid, common_name, birth_date, birth_place, person_uuid FROM fc_person", 
               "insert":"INSERT INTO fc_person(common_name, birth_date, birth_place) VALUES(%s,%s,%s) RETURNING sid",
               "delete":"DELETE FROM fc_person WHERE sid=%s",
               "load":"SELECT sid, common_name, birth_date, birth_place, person_uuid FROM fc_person WHERE sid=%s",
               "update_person":"UPDATE fc_person SET common_name=%s, birth_date=%s, birth_place=%s WHERE sid=%s"
               }
        
    def __init__(self, sid=None, common_name=None, birth_date=None, birth_place=None, person_uuid=None):
        super(Person, self).__init__(Person.sql_dict,sid,person_uuid)
        self.common_name=common_name
        self.birth_date=birth_date
        self.birth_place=birth_place
        if sid!=None:
            self.names=PersonName().get_all_for_foreign_key(self.sid)
        else:
            self.names=[]

       
    def load_object_from_db(self,rec):
        self.common_name=rec.common_name
        self.birth_date=rec.birth_date
        self.birth_place=rec.birth_place
        self.uuid=rec.person_uuid
        self.names=PersonName().get_all_for_foreign_key(self.sid)

       
    def get_insert_data(self):
        return (self.common_name,self.birth_date,self.birth_place)
       
       
    def insert(self):
        super(Person, self).insert()
        for name in self.names:
            name.person_sid=self.sid
            name.insert()
        get_db_connection().commit()
        
    
    def add_name(self, person_name_sid, person_name_role, person_sid, namepart_list):
        self.names.append(PersonName(person_name_sid, person_name_role, person_sid, namepart_list))
        
        
    def fabric_method(self,rec):
        return Person(rec.sid, rec.common_name, rec.birth_date, rec.birth_place, rec.person_uuid)           
        
        
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
        


