'''
Created on 24.05.2015

@author: vvladych
'''
from MDO import MDO

class ForecastPublication(MDO):
    
    sql_dict={"get_all":"SELECT sid, forecast_sid, publication_sid FROM fc_forecast_publication",
              "get_all_foreign_key":"SELECT sid, forecast_sid, publication_sid FROM fc_forecast_publication WHERE forecast_sid=%s",
              "delete":"DELETE FROM fc_forecast_publication WHERE sid=%s",
              "insert":"INSERT INTO fc_forecast_publication(forecast_sid, publication_sid) VALUES(%s, %s) RETURNING sid",
              "load":"SELECT sid, forecast_sid, publication_sid FROM fc_forecast_publication WHERE sid=%s"}
    
    def __init__(self, sid=None, uuid=None, forecast_sid=None, publication_sid=None):
        super(ForecastPublication, self).__init__(ForecastPublication.sql_dict,sid,uuid)
        self.forecast_sid=forecast_sid
        self.publication_sid=publication_sid
        

    def load_object_from_db(self,rec):
        self.forecast_sid=rec.forecast_sid
        self.publication_sid=rec.publication_sid
        
    def get_insert_data(self):
        return (self.forecast_sid, self.publication_sid,)
    
    def fabric_method(self,rec):
        return ForecastPublication(rec.sid, None, rec.forecast_sid, rec.publication_sid)