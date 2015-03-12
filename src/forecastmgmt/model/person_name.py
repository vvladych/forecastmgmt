
from forecastmgmt.dao.db_connection import get_db_connection


class PersonName:
    sql_dict={
              "insert_person_name":"INSERT INTO fc_person_name(fc_person_sid,name_role) VALUES(%s, %s) RETURNING sid",
              "update_person_name":"UPDATE fc_person_name SET name_role=%s WHERE sid=%s",
              "delete_person_name":"DELETE FROM fc_person_name WHERE sid=%s"
              }    
                
    def __init__(self, sid=None, name_role=None, person_sid=None, nameparts=[]):
        self.sid=sid
        self.name_role=name_role
        self.person_sid=person_sid
        self.nameparts=nameparts

    
    def __ne__(self, other):
        return not self==other

            
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__==other.__dict__
        else:
            return False

            
    
    def insert(self):
        cur = get_db_connection().cursor()
        data=(self.person_sid, self.name_role,)
        cur.execute(PersonName.sql_dict["insert_person_name"], data)
        self.sid=cur.fetchone()[0]
        for namepart in self.nameparts:
            namepart.person_name_sid=self.sid
            namepart.insert()
              
        
    def delete(self):
        cur = get_db_connection().cursor()
        data=(self.sid,)
        cur.execute(PersonName.sql_dict["delete_person_name"], data)
        cur.close()
        
        
    def add_namepart(self, namepart):
        self.nameparts.append(namepart)
