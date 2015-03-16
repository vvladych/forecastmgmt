'''
Created on 15.03.2015

@author: vvladych
'''

from forecastmgmt.dao.db_connection import get_db_connection
import psycopg2.extras

class FcProject:
    sql_dict={  "insert_project":"INSERT INTO fc_forecast(common_name) VALUES(%s) RETURNING sid",
                "delete_project":"DELETE FROM fc_forecast WHERE sid=%s"}
        
    def __init__(self, sid=None, common_name=None):
        self.sid=sid
        self.common_name=common_name
            
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__==other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self==other


    def insert(self):
        cur = get_db_connection().cursor()
        cur.execute(self.sql_dict["insert_project"],(self.common_name,))
        self.sid = cur.fetchone()[0]
        cur.close()    