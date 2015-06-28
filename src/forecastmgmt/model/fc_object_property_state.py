

from MDO import MDO


class FCObjectPropertyState(MDO):
    sql_dict={
              "insert":"INSERT INTO fc_object_property_state(object_property_sid,point_in_time,object_property_state_value,model_sid) VALUES(%s, %s, %s, %s) RETURNING sid",
              "delete":"DELETE FROM fc_object_property_state WHERE sid=%s",
              "get_all_foreign_key":"SELECT sid, object_property_sid,point_in_time,object_property_state_value,model_sid FROM fc_object_property_state WHERE model_sid=%s",
              }    
                
    def __init__(self, sid=None, object_property_sid=None, point_in_time=None, object_property_state_value=None, model_sid=None):
        super(FCObjectPropertyState, self).__init__(FCObjectPropertyState.sql_dict,sid,None)
        self.object_property_sid=object_property_sid
        self.point_in_time=point_in_time
        self.object_property_state_value=object_property_state_value
        self.model_sid=model_sid


    def get_insert_data(self):
        return (self.object_property_sid, self.point_in_time, self.object_property_state_value, self.model_sid,)
                
    def fabric_method(self,rec):
        return FCObjectPropertyState(rec.sid, rec.object_property_sid, rec.point_in_time, rec.object_property_state_value, rec.model_sid,)
    
