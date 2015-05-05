'''
Created on 02.05.2015

@author: vvladych
'''

from MDO import MDO

class Organisation(MDO):
    
    sql_dict={"get_all":"SELECT sid, common_name, organization_uuid FROM fc_organization",
              "delete":"DELETE FROM fc_organization WHERE sid=%s",
              "insert":"INSERT INTO fc_organization(common_name) VALUES(%s) RETURNING sid",
              "load":"SELECT common_name, organization_uuid FROM fc_organization WHERE sid=%s"}
    
    def __init__(self, sid=None, common_name=None, uuid=None):
        super(Organisation, self).__init__(Organisation.sql_dict,sid,uuid)
        self.common_name=common_name
        

    def load_object_from_db(self,rec):
        self.common_name=rec.common_name
        self.uuid=rec.organization_uuid
        
    def get_insert_data(self):
        return (self.common_name,)
    
    def fabric_method(self,rec):
        return Organisation(rec.sid, rec.common_name, rec.organization_uuid)
