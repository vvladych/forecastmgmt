
__author__="vvladych"
__date__ ="$09.10.2014 23:01:15$"

class Person:
    
    def __init__(self):
        self(None,None,None)
        
    def __init__(self, sid, common_name):
        self.sid=sid
        self.common_name=common_name
    
    
    def get_common_name(self):
        return self.common_name
    
    def set_common_name(self, common_name):
        self.common_name=common_name
        
        
    def get_sid(self):
        return self.sid
    
    def set_sid(self, sid):
        self.sid=sid

