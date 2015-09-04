

from MDO import MDO

from person_namepart import Namepart

class PersonName(MDO):
    sql_dict={
              "insert":"INSERT INTO fc_person_name(fc_person_sid,name_role) VALUES(%s, %s) RETURNING sid",
              "update":"UPDATE fc_person_name SET name_role=%s WHERE sid=%s",
              "delete":"DELETE FROM fc_person_name WHERE sid=%s",
              "get_all_foreign_key":"SELECT sid, name_role,fc_person_sid FROM fc_person_name WHERE fc_person_sid=%s",
              }    
                
    def __init__(self, sid=None, name_role=None, person_sid=None, nameparts=[]):
        super(PersonName, self).__init__(PersonName.sql_dict,sid,None)
        self.name_role=name_role
        self.person_sid=person_sid
        self.nameparts=nameparts


    def get_insert_data(self):
        print("hier: %s" % self.person_sid)
        return (self.person_sid, self.name_role,)
    
    def insert(self):
        super(PersonName, self).insert()
        for namepart in self.nameparts:
            namepart.person_name_sid=self.sid
            namepart.insert()
                
    def fabric_method(self,rec):
        return PersonName(rec.sid, rec.name_role, rec.fc_person_sid, Namepart().get_all_for_foreign_key(rec.sid))
                
    def add_namepart(self, namepart):
        self.nameparts.append(namepart)
