
__author__="vvladych"
__date__ ="$09.10.2014 23:01:15$"

class Person:
    
    def __init__(self):
        self(None,None,None,None,None,None)
        
    def __init__(self, sid, common_name, birth_date, birth_place, person_uuid):
        self.sid=sid
        self.common_name=common_name
        self.birth_date=birth_date
        self.birth_place=birth_place
        self.person_uuid=person_uuid
    
