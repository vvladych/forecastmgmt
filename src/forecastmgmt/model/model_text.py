'''
Created on 31.05.2015

@author: vvladych
'''
from MDO import MDO

from forecastmgmt.dao.db_connection import get_db_connection
import psycopg2.extras


class ModelText(MDO):
    
    sql_dict={"get_all":"SELECT sid, forecast_sid, model_text FROM fc_model_text",
              "delete":"DELETE FROM fc_model_text WHERE sid=%s",
              "insert":"INSERT INTO fc_model_text(forecast_sid, model_text) VALUES(%s, %s) RETURNING sid",
              "load":"SELECT forecast_sid, model_text FROM fc_model_text WHERE sid=%s",
              "update":"UPDATE fc_model_text SET model_text=%s WHERE sid=%s"}
    
    def __init__(self, sid=None, forecast_sid=None, model_text=None):
        super(ModelText, self).__init__(ModelText.sql_dict,sid,None)
        self.forecast_sid=forecast_sid
        self.model_text=model_text
        

    def load_object_from_db(self,rec):
        self.sid=rec.sid
        self.forecast_sid=rec.forecast_sid
        self.model_text=rec.model_text
        
    def get_insert_data(self):
        return (self.forecast_sid, self.model_text)
    
    def fabric_method(self,rec):
        return ModelText(rec.sid, rec.forecast_sid, rec.model_text)
    
    def update(self, model_text=None):
        cur=get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        data=(model_text, self.sid,)
        cur.execute(ModelText.sql_dict["update"], data)
        cur.close()
        get_db_connection().commit()