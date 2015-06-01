
from MDO import MDO

class FCObject(MDO):
    
    sql_dict={"get_all":"SELECT sid, common_name, uuid FROM fc_object",
              "delete":"DELETE FROM fc_object WHERE sid=%s",
              "insert":"INSERT INTO fc_object(common_name) VALUES(%s) RETURNING sid",
              "load":"SELECT common_name, uuid FROM fc_object WHERE sid=%s"}
    
    def __init__(self, sid=None, common_name=None, uuid=None):
        super(FCObject, self).__init__(FCObject.sql_dict,sid,uuid)
        self.common_name=common_name
        

    def load_object_from_db(self,rec):
        self.common_name=rec.common_name
        self.uuid=rec.uuid
        
    def get_insert_data(self):
        return (self.common_name,)
    
    def fabric_method(self,rec):
        return FCObject(rec.sid, rec.common_name, rec.uuid)
