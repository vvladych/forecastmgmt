

__author__="vvladych"
__date__ ="$09.10.2014 23:01:15$"

class Namepart:
    
    def __init__(self):
        self(None,None,None,None,None)

    def __init__(self, sid, namepart_role, namepart_value, person_name_sid):
        self.sid=sid
        self.namepart_role=namepart_role
        self.namepart_value=namepart_value
        self.person_name_sid=person_name_sid


