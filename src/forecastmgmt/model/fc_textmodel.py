'''
Created on 17.03.2015

@author: vvladych
'''
from forecastmgmt.dao.db_connection import get_db_connection
import psycopg2.extras

from MDO import MDO

class FCTextModel(MDO):
    
    
    sql_dict={"get_all":"SELECT sid, textmodel_date, textmodel_uuid, forecast_sid FROM fc_textmodel",
              "delete":"DELETE FROM fc_textmodel WHERE sid=%s",
              "insert":"INSERT INTO fc_textmodel(textmodel_date, forecast_sid) VALUES(%s,%s) RETURNING sid",
              "load":"SELECT sid, textmodel_date, textmodel_uuid, forecast_sid FROM fc_textmodel WHERE sid=%s",
              "get_all_foreign_key":"SELECT sid, textmodel_uuid, textmodel_date, forecast_sid FROM fc_textmodel WHERE forecast_sid=%s",
              }
    
    def __init__(self, sid=None, uuid=None, textmodel_date=None, forecast_sid=None):
        super(FCTextModel, self).__init__(FCTextModel.sql_dict,sid,uuid)
        self.textmodel_date=textmodel_date
        self.forecast_sid=forecast_sid
        

    def get_insert_data(self):
        return (self.textmodel_date, self.forecast_sid)
                
    def fabric_method(self,rec):
        return FCTextModel(rec.sid, rec.textmodel_uuid, rec.textmodel_date,  rec.forecast_sid)
