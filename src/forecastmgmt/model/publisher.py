'''
Created on 04.05.2015

@author: vvladych
'''

from MDO import MDO

class Publisher(MDO):
    
    sql_dict={"get_all":"SELECT sid, publisher_common_name, publisher_uuid FROM fc_publisher",
              "delete":"DELETE FROM fc_publisher WHERE sid=%s",
              "insert":"INSERT INTO fc_publisher(publisher_common_name) VALUES(%s) RETURNING sid",
              "load":"SELECT publisher_common_name, publisher_uuid FROM fc_publisher WHERE sid=%s"}
    
    def __init__(self, sid=None, common_name=None, uuid=None):
        super(Publisher, self).__init__(Publisher.sql_dict,sid,uuid)
        self.common_name=common_name
        

    def load_object_from_db(self,rec):
        self.common_name=rec.publisher_common_name
        self.uuid=rec.publisher_uuid
        
    def get_insert_data(self):
        return (self.common_name,)
    
    def fabric_method(self,rec):
        return Publisher(rec.sid, rec.publisher_common_name, rec.publisher_uuid)
        