
__author__="vvladych"
__date__ ="$10.02.2015 23:01:15$"

class PersonName:
    
    def __init__(self):
        self(None,None,None)
        
    def __init__(self, sid, name_role, person_sid):
        self.sid=sid
        self.name_role=name_role
        self.person_sid=person_sid

    def set_sid(self,sid):
       self.sid=sid
