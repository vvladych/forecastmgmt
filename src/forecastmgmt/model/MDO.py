'''
Created on 05.05.2015

@author: vvladych
'''
# Master Data Object, abstract class


from forecastmgmt.dao.db_connection import get_db_connection
import psycopg2.extras


class MDO(object):
    
    def __init__(self, sql_dict,sid=None, uuid=None):
        self.sql_dict=sql_dict
        self.sid=sid
        self.uuid=uuid
        

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__==other.__dict__
        else:
            return False
        
    def __ne__(self, other):
        return not self==other
    
    def insert(self):
        cur = get_db_connection().cursor()        
        cur.execute(self.sql_dict["insert"],self.get_insert_data())
        self.sid=cur.fetchone()[0]
        cur.close()
        get_db_connection().commit()
        
    def get_insert_data(self):
        raise NotImplementedError("get_insert_data still not implemented!")
        
    def delete(self,sqlstmt,data):
        cur = get_db_connection().cursor()
        cur.execute(self.sql_dict["delete"],self.get_delete_data())
        cur.close()
        get_db_connection().commit()
        
    # default implementation
    def get_delete_data(self):
        return (self.sid,)
    
    def load(self):
        cur=get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        data=(self.sid,)
        cur.execute(self.sql_dict["load"],data)
        for p in cur.fetchall():
            self.load_object_from_db(p)
        cur.close()

    def load_object_from_db(self, rec):
        raise NotImplementedError("load_object_from_db still not implemented!")

        