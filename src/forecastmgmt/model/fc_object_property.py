

from MDO import MDO


class FCObjectProperty(MDO):
    sql_dict={
              "insert":"INSERT INTO fc_object_property(object_sid,common_name) VALUES(%s, %s) RETURNING sid",
              "update":"UPDATE fc_object_property SET common_name=%s WHERE sid=%s",
              "delete":"DELETE FROM fc_object_property WHERE sid=%s",
              "get_all_foreign_key":"SELECT sid, uuid, common_name, object_sid FROM fc_object_property WHERE object_sid=%s",
              }    
                
    def __init__(self, sid=None, uuid=None, common_name=None, object_sid=None):
        super(FCObjectProperty, self).__init__(FCObjectProperty.sql_dict,sid,uuid)
        self.common_name=common_name
        self.object_sid=object_sid


    def get_insert_data(self):
        return (self.object_sid, self.common_name,)
                
    def fabric_method(self,rec):
        return FCObjectProperty(rec.sid, rec.uuid, rec.common_name, rec.object_sid)
                
