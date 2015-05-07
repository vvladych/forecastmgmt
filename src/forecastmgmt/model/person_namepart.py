
from MDO import MDO

class Namepart(MDO):
    
    sql_dict={  "insert":"INSERT INTO fc_person_name_part(name_part_role, name_part_value, person_name_sid) VALUES(%s, %s, %s) RETURNING sid",
                "delete":"DELETE FROM fc_person_name_part WHERE sid=%s"}
        
    def __init__(self, sid=None, namepart_role=None, namepart_value=None, person_name_sid=None):
        super(Namepart, self).__init__(Namepart.sql_dict,sid,None)
        self.namepart_role=namepart_role
        self.namepart_value=namepart_value
        self.person_name_sid=person_name_sid
            
    def get_insert_data(self):
        return (self.namepart_role, self.namepart_value, self.person_name_sid,)
    