
from MDO import MDO
from fc_object_property import FCObjectProperty

class FCObject(MDO):
    
    sql_dict={"get_all":"SELECT sid, common_name, uuid FROM fc_object",
              "delete":"DELETE FROM fc_object WHERE sid=%s",
              "insert":"INSERT INTO fc_object(common_name) VALUES(%s) RETURNING sid",
              "load":"SELECT common_name, uuid FROM fc_object WHERE sid=%s"}
    
    def __init__(self, sid=None, common_name=None, uuid=None):
        super(FCObject, self).__init__(FCObject.sql_dict,sid,uuid)
        self.common_name=common_name
        if self.sid!=None:
            self.object_properties=FCObjectProperty().get_all_for_foreign_key(self.sid)
        else:
            self.object_properties=[]
        

    def load_object_from_db(self,rec):
        self.common_name=rec.common_name
        self.uuid=rec.uuid
        self.object_properties=FCObjectProperty().get_all_for_foreign_key(self.sid)
        
    def get_insert_data(self):
        return (self.common_name,)
    
    def fabric_method(self,rec):
        return FCObject(rec.sid, rec.common_name, rec.uuid)
    
    def insert(self):
        super(FCObject, self).insert()
        for object_property in self.object_properties:
            object_property.object_sid=self.sid
            object_property.insert()
        get_db_connection().commit()
        
    def add_object_property(self, object_property_sid, object_property_common_name, object_sid):
        self.object_properties.append(FCObjectProperty(object_property_sid, object_property_common_name, object_sid))
        
