'''
Created on 14.05.2015

@author: vvladych
'''

from MDO import MDO

class ForecastOriginator(MDO):
    
    sql_dict={"get_all":"SELECT sid, forecast_sid, originator_sid FROM fc_forecast_originator",
              "get_all_foreign_key":"SELECT sid, forecast_sid, originator_sid FROM fc_forecast_originator WHERE forecast_sid=%s",
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