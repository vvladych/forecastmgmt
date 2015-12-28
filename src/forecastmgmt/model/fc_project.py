'''
Created on 15.03.2015

@author: vvladych
'''


from src.forecastmgmt.model.MDO import MDO

from src.forecastmgmt.model.model_text import ModelText

from src.forecastmgmt.dao.db_connection import get_db_connection
import psycopg2.extras

class FcProject(MDO):
    sql_dict={  "insert":"INSERT INTO fc_forecast(common_name, short_description) VALUES(%s,%s) RETURNING sid",
                "delete":"DELETE FROM fc_forecast WHERE sid=%s",
                #"get_all":"SELECT sid, forecast_uuid, common_name, created_date FROM fc_forecast",
                "get_all":"SELECT 1 as sid, 1 as forecast_uuid, 't' as common_name, NULL as created_date",
                "get_forecast_models":"SELECT sid, model_date, model_uuid FROM fc_forecast WHERE forecast_sid=%s",
                "get_forecast_publications":"SELECT",
                "get_forecast_model_text":"SELECT sid,model_text FROM fc_model_text WHERE forecast_sid=%s",
                "load":"SELECT forecast_uuid,common_name,created_date,short_description FROM fc_forecast WHERE sid=%s"}
        
    def __init__(self, sid=None, forecast_uuid=None, common_name=None, created_date=None, short_description=None):
        super(FcProject, self).__init__(FcProject.sql_dict,sid,forecast_uuid)
        self.common_name=common_name
        self.created_date=created_date
        self.short_description=short_description
        if self.sid!=None:
            self._load_project_models()
            self.load_model_text()
            

    def get_insert_data(self):
        return (self.common_name,self.short_description,)        
        
        
    def load_object_from_db(self,rec):
        self.common_name=rec.common_name
        self.uuid=rec.forecast_uuid
        self.created_date=rec.created_date
        self.short_description=rec.short_description
        self._load_project_models()
        self._load_project_publications()
        
        
    def _load_project_models(self):
        self.models=[]
        
        
    def _load_project_publications(self):
        self.publications=[]
        
    def load_model_text(self):
        self.model_text=None
        cur=get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        data=(self.sid,)
        #cur.execute("""SELECT
        #                sid, model_text
        #                FROM
        #                fc_model_text
        #                WHERE
        #                forecast_sid=%s
        #                """,data)
        cur.execute("SELECT 1 as sid, 'text' as model_text")
        for p in cur.fetchall():
            self.model_text=ModelText(sid=p.sid, model_text=p.model_text, forecast_sid=self.sid)
        cur.close()        

        
    def fabric_method(self,rec):
        return FcProject(rec.sid, rec.forecast_uuid, rec.common_name, rec.created_date)

        

