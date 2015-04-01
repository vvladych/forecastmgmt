'''
Created on 15.03.2015

@author: vvladych
'''

from forecastmgmt.dao.db_connection import get_db_connection
import psycopg2.extras

class FcProject:
    sql_dict={  "insert_forecast":"INSERT INTO fc_forecast(common_name) VALUES(%s) RETURNING sid",
                "delete_forecast":"DELETE FROM fc_forecast WHERE sid=%s",
                "get_forecast_list":"SELECT sid, forecast_uuid, common_name, created_date FROM fc_forecast",
                "get_forecast_models":"SELECT sid, model_date, model_uuid FROM fc_forecast WHERE forecast_sid=%s",
                "get_forecast_publications":"SELECT",
                "load_forecast":"SELECT forecast_uuid FROM fc_forecast WHERE sid=%s"}
        
    def __init__(self, sid=None, forecast_uuid=None, common_name=None, created_date=None):
        self.sid=sid
        self.forecast_uuid=forecast_uuid
        self.common_name=common_name
        self.created_date=created_date
        if self.sid!=None:
            self._load_project_models()
            
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__==other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self==other


    def insert(self):
        cur = get_db_connection().cursor()
        cur.execute(self.sql_dict["insert_forecast"],(self.common_name,))
        self.sid = cur.fetchone()[0]
        cur.close()  
        get_db_connection().commit()
        

    def load(self):
        cur=get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        data=(self.sid,)
        cur.execute(FcProject.sql_dict["load_forecast"],data)
        for p in cur.fetchall():
            self.forecast_uuid=p.forecast_uuid
            self._load_project_models()
            self._load_project_publications()
        cur.close()
        
        
    def _load_project_models(self):
        self.models=[]
        
        
    def _load_project_publications(self):
        self.publications=[]
        
        
def get_project_list():
    projectlist=[]
    cur = get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cur.execute(FcProject.sql_dict["get_forecast_list"])
    for forecast in cur.fetchall():
        projectlist.append(FcProject(forecast.sid, forecast.forecast_uuid, forecast.common_name, forecast.created_date))
    cur.close()
    return projectlist
