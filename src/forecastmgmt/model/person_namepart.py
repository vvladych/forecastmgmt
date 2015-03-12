from forecastmgmt.dao.db_connection import get_db_connection

class Namepart:
    
    sql_dict={  "insert_namepart":"INSERT INTO fc_person_name_part(name_part_role, name_part_value, person_name_sid) VALUES(%s, %s, %s) RETURNING sid",
                "delete_namepart":"DELETE FROM fc_person_name_part WHERE sid=%s"}
        
    def __init__(self, sid=None, namepart_role=None, namepart_value=None, person_name_sid=None):
        self.sid=sid
        self.namepart_role=namepart_role
        self.namepart_value=namepart_value
        self.person_name_sid=person_name_sid
            
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__==other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self==other


    def insert(self):
        cur = get_db_connection().cursor()
        cur.execute(Namepart.sql_dict["insert_namepart"],(self.namepart_role, self.namepart_value, self.person_name_sid,))
        self.sid = cur.fetchone()[0]
        cur.close()

    def delete(self):
        cur = get_db_connection().cursor()
        cur.execute(Namepart.sql_dict["delete_namepart"],(self.sid,))
        cur.close()
        

    
