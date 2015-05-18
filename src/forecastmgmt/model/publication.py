'''
Created on 18.05.2015

@author: vvladych
'''

from MDO import MDO

class Publication(MDO):

    sql_dict={"get_all":"SELECT sid, publisher_sid, uuid, publishing_date, title FROM fc_publication",
              "delete":"DELETE FROM fc_publication WHERE sid=%s",
              "insert":"INSERT INTO fc_publication(publisher_sid,publishing_date,title) VALUES(%s,%s,%s) RETURNING sid",
              "load":"SELECT title, uuid FROM fc_publication WHERE sid=%s"}
    
    def __init__(self, sid=None, uuid=None, publisher_sid=None, publishing_date=None, title=None):
        super(Publication, self).__init__(Publication.sql_dict,sid,uuid)
        self.publisher_sid=publisher_sid
        self.publishing_date=publishing_date
        self.title=title
        

    def load_object_from_db(self,rec):
        self.publisher_sid=rec.publisher_sid
        self.uuid=rec.uuid
        self.publishing_date=rec.publishing_date
        self.title=rec.title
        
    def get_insert_data(self):
        return (self.publisher_sid,self.publishing_date,self.title,)
    
    def fabric_method(self,rec):
        return Publication(rec.sid, rec.uuid, rec.publisher_sid, rec.publisher_date, rec.title)
    
