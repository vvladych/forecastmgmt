'''
Created on 02.05.2015

@author: vvladych
'''
from forecastmgmt.dao.db_connection import get_db_connection
import psycopg2.extras


class Organisation:
    
    sql_dict={"get_all_organisations":"SELECT sid, common_name, organization_uuid FROM fc_organization",
              "delete_organisation":"DELETE FROM fc_organization WHERE sid=%s",
              "insert_organisation":"INSERT INTO fc_organization(common_name) VALUES(%s) RETURNING sid"}
    
    def __init__(self, sid=None, common_name=None, organisation_uuid=None):
        self.sid=sid
        self.common_name=common_name
        self.organisation_uuid=organisation_uuid
        
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
        cur.execute(Organisation.sql_dict["load_organisation"],data)
        for p in cur.fetchall():
            self.common_name=p.common_name
            self.organisation_uuid=p.organisation_uuid
        cur.close()
        
        
    def insert(self):
        cur = get_db_connection().cursor()
        data=(self.common_name,)
        cur.execute(Organisation.sql_dict["insert_organisation"],data)
        self.sid=cur.fetchone()[0]
        cur.close()
        get_db_connection().commit()
        
        
    def delete(self):
        cur = get_db_connection().cursor()
        data=(self.sid,)
        cur.execute(Organisation.sql_dict["delete_organisation"],data)
        cur.close()
        get_db_connection().commit()


    
def get_all_organisations():
    organisationlist=[]
    cur = get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cur.execute(Organisation.sql_dict["get_all_organisations"])
    for organisation in cur.fetchall():
        organisationlist.append(Organisation(organisation.sid, organisation.common_name, organisation.organization_uuid))
    cur.close()
    return organisationlist