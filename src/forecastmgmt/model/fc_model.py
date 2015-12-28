'''
Created on 17.03.2015

@author: vvladych
'''
from src.forecastmgmt.dao.db_connection import get_db_connection
import psycopg2.extras

from src.forecastmgmt.model.MDO import MDO

class FCModel(MDO):
    
    
    sql_dict={"get_all":"SELECT sid, model_date, model_uuid, forecast_sid FROM fc_model",
              "delete":"DELETE FROM fc_model WHERE sid=%s",
              "insert":"INSERT INTO fc_model(model_date, forecast_sid) VALUES(%s,%s) RETURNING sid",
              "load":"SELECT sid, model_date, model_uuid, forecast_sid FROM fc_model WHERE sid=%s",
              "get_all_foreign_key":"SELECT sid, model_uuid, model_date, forecast_sid FROM fc_model WHERE forecast_sid=%s",
              }
    
    def __init__(self, sid=None, uuid=None, model_date=None, forecast_sid=None):
        super(FCModel, self).__init__(FCModel.sql_dict,sid,uuid)
        self.model_date=model_date
        self.forecast_sid=forecast_sid
        

    def get_insert_data(self):
        return (self.model_date, self.forecast_sid)
                
    def fabric_method(self,rec):
        return FCModel(rec.sid, rec.model_uuid, rec.model_date,  rec.forecast_sid)
