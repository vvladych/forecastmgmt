'''
Created on 15.03.2015

@author: vvladych
'''


from MDO import MDO

class FcProject(MDO):
    sql_dict={  "insert":"INSERT INTO fc_forecast(common_name, short_description) VALUES(%s,%s) RETURNING sid",
                "delete":"DELETE FROM fc_forecast WHERE sid=%s",
                "get_all":"SELECT sid, forecast_uuid, common_name, created_date FROM fc_forecast",
                "get_forecast_models":"SELECT sid, model_date, model_uuid FROM fc_forecast WHERE forecast_sid=%s",
                "get_forecast_publications":"SELECT",
                "load":"SELECT forecast_uuid,common_name,created_date,short_description FROM fc_forecast WHERE sid=%s"}
        
    def __init__(self, sid=None, forecast_uuid=None, common_name=None, created_date=None, short_description=None):
        super(FcProject, self).__init__(FcProject.sql_dict,sid,forecast_uuid)
        self.common_name=common_name
        self.created_date=created_date
        self.short_description=short_description
        if self.sid!=None:
            self._load_project_models()
            

    def get_insert_data(self):
        return (self.common_name,)        
        
        
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
        
    def fabric_method(self,rec):
        return FcProject(rec.sid, rec.forecast_uuid, rec.common_name, rec.created_date)

        

