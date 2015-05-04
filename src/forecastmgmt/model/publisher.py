'''
Created on 04.05.2015

@author: vvladych
'''
from forecastmgmt.dao.db_connection import get_db_connection
import psycopg2.extras


class Publisher:
    
    sql_dict={"get_all_publishers":"SELECT sid, publisher_common_name, publisher_uuid FROM fc_publisher",
              "delete_publisher":"DELETE FROM fc_publisher WHERE sid=%s",
              "insert_publisher":"INSERT INTO fc_publisher(publisher_common_name) VALUES(%s) RETURNING sid"}
    
    def __init__(self, sid=None, common_name=None, publisher_uuid=None):
        self.sid=sid
        self.common_name=common_name
        self.publisher_uuid=publisher_uuid
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__==other.__dict__
        else:
            return False
        
    def __ne__(self, other):
        return not self==other


    def load(self):
        cur=get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        data=(self.sid,)
        cur.execute(Publisher.sql_dict["load_publisher"],data)
        for p in cur.fetchall():
            self.common_name=p.common_name
            self.publisher_uuid=p.publisher_uuid
        cur.close()
        
        
    def insert(self):
        cur = get_db_connection().cursor()
        data=(self.common_name,)
        cur.execute(Publisher.sql_dict["insert_publisher"],data)
        self.sid=cur.fetchone()[0]
        cur.close()
        get_db_connection().commit()
        
    def delete(self):
        cur = get_db_connection().cursor()
        data=(self.sid,)
        cur.execute(Publisher.sql_dict["delete_publisher"],data)
        cur.close()
        get_db_connection().commit()


    
def get_all_publishers():
    publisherlist=[]
    cur = get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cur.execute(Publisher.sql_dict["get_all_publishers"])
    for publisher in cur.fetchall():
        publisherlist.append(Publisher(publisher.sid, publisher.publisher_common_name, publisher.publisher_uuid))
    cur.close()
    return publisherlist