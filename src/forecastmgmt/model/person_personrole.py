'''
Created on 02.09.2015

@author: vvladych
'''
from MDO import MDO


class PersonPersonrole(MDO):
    sql_dict={
              "insert":"INSERT INTO fc_person_personrole(person_sid,personrole_sid) VALUES(%s, %s) RETURNING sid",
              "update":"",
              "delete":"DELETE FROM fc_person_personrole WHERE sid=%s",
              "get_all_foreign_key":"""SELECT fpp.sid as sid, fp.sid as person_sid, fp.sid as personrole_sid, fp.uuid, fp.common_name 
                                      FROM fc_person_personrole fpp, fc_personrole fp 
                                      WHERE 
                                      fpp.personrole_sid=fp.sid AND person_sid=%s"""
              }    
                
    def __init__(self, sid=None, person_sid=None, personrole_sid=None):
        super(PersonPersonrole, self).__init__(PersonPersonrole.sql_dict,sid,None)
        self.person_sid=person_sid
        self.personrole_sid=personrole_sid


    def get_insert_data(self):
        return (self.person_sid, self.personrole_sid,)
    
                
    def fabric_method(self,rec):
        return PersonPersonrole(rec.sid, rec.person_sid, rec.personrole_sid)
