'''
Created on 04.05.2015

@author: vvladych
'''
from forecastmgmt.dao.db_connection import get_db_connection
import psycopg2.extras

from MDO import MDO

class Publisher(MDO):
    
    sql_dict={"get_all":"SELECT sid, publisher_common_name, publisher_url, publisher_uuid FROM fc_publisher",
              "delete":"DELETE FROM fc_publisher WHERE sid=%s",
              "insert":"INSERT INTO fc_publisher(publisher_common_name, publisher_url) VALUES(%s, %s) RETURNING sid",
              "load":"SELECT publisher_common_name, publisher_url, publisher_uuid FROM fc_publisher WHERE sid=%s",
              "update_publisher":"UPDATE fc_publisher SET publisher_common_name=%s, publisher_url=%s WHERE sid=%s"}
    
    def __init__(self, sid=None, uuid=None, common_name=None, url=None):
        super(Publisher, self).__init__(Publisher.sql_dict,sid,uuid)
        self.common_name=common_name
        self.url=url
        

    def load_object_from_db(self,rec):
        self.common_name=rec.publisher_common_name
        self.uuid=rec.publisher_uuid
        self.url=rec.publisher_url
        
    def get_insert_data(self):
        return (self.common_name,self.url,)
    
    def fabric_method(self,rec):
        return Publisher(rec.sid, rec.publisher_uuid, rec.publisher_common_name, rec.publisher_url)
    
    def update(self, other):
        cur=get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        data=(other.common_name, other.url, self.sid)
        cur.execute(Publisher.sql_dict["update_publisher"],data)
        cur.close()
        
        get_db_connection().commit()
        