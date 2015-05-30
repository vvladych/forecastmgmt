'''
Created on 31.05.2015

@author: vvladych
'''
from MDO import MDO

class ModelText(MDO):
    
    sql_dict={"get_all":"SELECT sid, forecast_sid, text FROM fc_model_text",
              "delete":"DELETE FROM fc_model_text WHERE sid=%s",
              "insert":"INSERT INTO fc_model_text(forecast_sid, text) VALUES(%s, %s) RETURNING sid",
              "load":"SELECT forecast_sid, text FROM fc_model_text WHERE sid=%s"}
    
    def __init__(self, sid=None, forecast_sid=None, text=None):
        super(ModelText, self).__init__(ModelText.sql_dict,sid,None)
        self.forecast_sid=forecast_sid
        self.text=text
        

    def load_object_from_db(self,rec):
        self.forecast_sid=rec.forecast_sid
        self.text=rec.text
        
    def get_insert_data(self):
        return (self.forecast_sid, self.text)
    
    def fabric_method(self,rec):
        return ModelText(rec.sid, rec.forecast_sid, rec.text)
