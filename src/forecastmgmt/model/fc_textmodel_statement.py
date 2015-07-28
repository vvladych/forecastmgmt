'''
Created on 29.07.2015

@author: vvladych
'''

from MDO import MDO

class FCTextmodelStatement(MDO):
    sql_dict={
              "insert":"INSERT INTO fc_textmodel_statement(statement_text,point_in_time,textmodel_sid) VALUES(%s, daterange(%s,%s), %s) RETURNING sid",
              "update":"",
              "delete":"DELETE FROM fc_textmodel_statement WHERE sid=%s",
              "get_all_foreign_key":"SELECT sid, uuid, statement_text, point_in_time, textmodel_sid FROM fc_textmodel_statement WHERE textmodel_sid=%s",
              } 
    
    
    def __init__(self, sid=None, uuid=None, statement_text=None, point_in_time_begin=None, point_in_time_end=None, textmodel_sid=None):
        super(FCTextmodelStatement, self).__init__(FCTextmodelStatement.sql_dict,sid,uuid)
        self.statement_text=statement_text
        self.point_in_time_begin=point_in_time_begin
        self.point_in_time_end=point_in_time_end
        self.textmodel_sid=textmodel_sid
        

    def get_insert_data(self):
        return (self.statement_text, self.point_in_time_begin, self.point_in_time_end, self.textmodel_sid,)
                
    def fabric_method(self,rec):
        r=rec.point_in_time
        return FCTextmodelStatement(rec.sid, rec.uuid, rec.statement_text, r.lower, r.upper, rec.textmodel_sid,)
    