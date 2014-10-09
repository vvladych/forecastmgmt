
__author__="vvladych"
__date__ ="$09.10.2014 23:01:15$"

class Person:
    
    def __init__(self):
        self(None,None,None)
        
    def __init__(self, sid, common_name):
        self.__sid=sid
        self.__common_name=common_name
    
    
    def get_common_name(self):
        return self.__common_name
    
    def set_common_name(self, common_name):
        self.__common_name=common_name
        
        
    def get_sid(self):
        return self.__sid
    
    def set_id(self, sid):
        self.__sid=sid

