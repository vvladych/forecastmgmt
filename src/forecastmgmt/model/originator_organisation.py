'''
Created on 20.05.2015

@author: vvladych
'''
from src.forecastmgmt.model.MDO import MDO

class OriginatorOrganisation(MDO):
    
    sql_dict={"get_all":"",
          "get_all_foreign_key":"",
          "delete":"DELETE FROM fc_originator_organisation WHERE sid=%s",
          "insert":"INSERT INTO fc_originator_organisation(originator_sid, organisation_sid) VALUES(%s, %s) RETURNING sid",
          "load":"SELECT sid, originator_sid, organisation_sid FROM fc_originator_organisation WHERE sid=%s"}
    
    def __init__(self, sid=None, uuid=None, originator_sid=None, organisation_sid=None):
        super(OriginatorOrganisation, self).__init__(OriginatorOrganisation.sql_dict,sid,uuid)
        self.originator_sid=originator_sid
        self.organisation_sid=organisation_sid
        

    def load_object_from_db(self,rec):
        self.originator_sid=rec.originator_sid
        self.organisation_sid=rec.organisation_sid
        
    def get_insert_data(self):
        return (self.originator_sid, self.organisation_sid,)
    
    def fabric_method(self,rec):
        return OriginatorOrganisation(rec.sid, None, rec.originator_sid, rec.organisation_sid)