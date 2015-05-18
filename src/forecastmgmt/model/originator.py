'''
Created on 14.05.2015

@author: vvladych
'''

from MDO import MDO

class Originator(MDO):
    
    sql_dict={"get_all":"SELECT sid, originator_uuid FROM fc_originator",
              "delete":"DELETE FROM fc_originator WHERE sid=%s",
              "insert":"INSERT INTO fc_originator(originator_common_name) VALUES(%s) RETURNING sid",
              "load":"SELECT sid, originator_uuid FROM fc_originator WHERE sid=%s"}
    
    def __init__(self, sid=None, common_name=None, uuid=None):
        super(Originator, self).__init__(Originator.sql_dict,sid,uuid)
        self.common_name=common_name
        

    def load_object_from_db(self,rec):
        self.uuid=rec.originator_uuid
        
    def get_insert_data(self):
        return ("",)
    
    def fabric_method(self,rec):
        return Originator(rec.sid, rec.originator_uuid)