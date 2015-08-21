'''
Created on 14.05.2015

@author: vvladych
'''

from MDO import MDO

class ForecastOriginator(MDO):
    
    sql_dict={"get_all":"SELECT sid, forecast_sid, originator_sid FROM fc_forecast_originator",
              #"get_all_foreign_key":"SELECT sid, forecast_sid, originator_sid FROM fc_forecast_originator WHERE forecast_sid=%s",
              "get_all_foreign_key":"""SELECT 
                        fc_person.sid as sid, forecast_sid, fc_person.common_name, fc_originator_person.originator_sid,'person' as origin_type 
                        FROM 
                        fc_forecast_originator, fc_originator_person, fc_person 
                        WHERE
                        fc_forecast_originator.forecast_sid=%s AND 
                        fc_forecast_originator.originator_sid=fc_originator_person.originator_sid AND
                        fc_originator_person.person_sid=fc_person.sid
                        UNION
                        SELECT 
                        fc_organization.sid as sid, forecast_sid, fc_organization.common_name, fc_originator_organisation.originator_sid,'organisation'  as origin_type  
                        FROM 
                        fc_forecast_originator, fc_originator_organisation, fc_organization
                        WHERE
                        fc_forecast_originator.forecast_sid=%s AND 
                        fc_forecast_originator.originator_sid=fc_originator_organisation.originator_sid AND
                        fc_originator_organisation.organisation_sid=fc_organization.sid
                        """,
              "delete":"DELETE FROM fc_forecast_originator WHERE sid=%s",
              "insert":"INSERT INTO fc_forecast_originator(forecast_sid, originator_sid) VALUES(%s, %s) RETURNING sid",
              "load":"SELECT sid, forecast_sid, originator_sid FROM fc_forecast_originator WHERE sid=%s"}
    
    def __init__(self, sid=None, uuid=None, forecast_sid=None, originator_sid=None):
        super(ForecastOriginator, self).__init__(ForecastOriginator.sql_dict,sid,uuid)
        self.forecast_sid=forecast_sid
        self.originator_sid=originator_sid
        

    def load_object_from_db(self,rec):
        self.forecast_sid=rec.forecast_sid
        self.originator_sid=rec.originator_sid
        
    def get_insert_data(self):
        return (self.forecast_sid, self.originator_sid,)
    
    def fabric_method(self,rec):
        return ForecastOriginator(rec.sid, None, rec.forecast_sid, rec.originator_sid)