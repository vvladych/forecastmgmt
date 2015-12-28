

from src.forecastmgmt.model.MDO import MDO

from psycopg2.extras import DateRange


class FCObjectPropertyState(MDO):
    sql_dict={
              "insert":"""INSERT INTO 
                          fc_object_property_state(object_property_sid,point_in_time,object_property_state_value,model_sid) 
                          VALUES(%s, daterange(%s,%s), %s, %s) 
                          RETURNING sid""",
              "delete":"DELETE FROM fc_object_property_state WHERE sid=%s",
              "get_all_foreign_key":"SELECT sid, object_property_sid,point_in_time,object_property_state_value,model_sid FROM fc_object_property_state WHERE model_sid=%s",
              }    
                
    def __init__(self, sid=None, object_property_sid=None, point_in_time_begin=None, point_in_time_end=None, object_property_state_value=None, model_sid=None):
        super(FCObjectPropertyState, self).__init__(FCObjectPropertyState.sql_dict,sid,None)
        self.object_property_sid=object_property_sid
        self.point_in_time_begin=point_in_time_begin
        self.point_in_time_end=point_in_time_end
        self.object_property_state_value=object_property_state_value
        self.model_sid=model_sid


    def get_insert_data(self):
        return (self.object_property_sid, self.point_in_time_begin, self.point_in_time_end, self.object_property_state_value, self.model_sid,)
                
    def fabric_method(self,rec):
        r=rec.point_in_time
        return FCObjectPropertyState(rec.sid, rec.object_property_sid, r.point_in_time.lower, r.point_in_time.upper, rec.object_property_state_value, rec.model_sid,)
    
