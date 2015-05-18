'''
Created on 15.05.2015

@author: vvladych
'''
from MDO import MDO

class OriginatorPerson(MDO):
    
    sql_dict={"get_all":"",
          "get_all_foreign_key":"",
          "delete":"DELETE FROM fc_originator_person WHERE sid=%s",
          "insert":"INSERT INTO fc_originator_person(originator_sid, person_sid) VALUES(%s, %s) RETURNING sid",
          "load":"SELECT sid, originator_sid, person_sid FROM fc_originator_person WHERE sid=%s"}
    
    def __init__(self, sid=None, uuid=None, originator_sid=None, person_sid=None):
        super(OriginatorPerson, self).__init__(OriginatorPerson.sql_dict,sid,uuid)
        self.originator_sid=originator_sid
        self.person_sid=person_sid
        

    def load_object_from_db(self,rec):
        self.originator_sid=rec.originator_sid
        self.person_sid=rec.person_sid
        
    def get_insert_data(self):
        return (self.originator_sid, self.person_sid,)
    
    def fabric_method(self,rec):
        return OriginatorPerson(rec.sid, None, rec.originator_sid, rec.person_sid)