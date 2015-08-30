'''
Created on 30.08.2015

@author: vvladych
'''
from MDO import MDO

class Personrole(MDO):
    
    sql_dict={"get_all":"SELECT sid, common_name, uuid FROM fc_personrole",
              "delete":"DELETE FROM fc_personrole WHERE sid=%s",
              "insert":"INSERT INTO fc_personrole(common_name) VALUES(%s) RETURNING sid",
              "load":"SELECT common_name, uuid FROM fc_organization WHERE sid=%s"}
    
    def __init__(self, sid=None, common_name=None, uuid=None):
        super(Personrole, self).__init__(Personrole.sql_dict,sid,uuid)
        self.common_name=common_name
        

    def load_object_from_db(self,rec):
        self.common_name=rec.common_name
        self.uuid=rec.uuid
        
    def get_insert_data(self):
        return (self.common_name,)
    
    def fabric_method(self,rec):
        return Personrole(rec.sid, rec.common_name, rec.uuid)