'''
Created on 16.05.2015

@author: vvladych
'''
from forecastmgmt.ui.forecast.forecast_abstract_add_area import AbstractAddArea

from gi.repository import Gtk

from forecastmgmt.ui.ui_tools import add_column_to_treeview
from forecastmgmt.model.person import Person


from forecastmgmt.model.originator import Originator
from forecastmgmt.model.forecast_originator import ForecastOriginator
from forecastmgmt.model.originator_person import OriginatorPerson
from forecastmgmt.dao.db_connection import get_db_connection
import psycopg2.extras



class OriginatorPersonAddArea(AbstractAddArea):
    
    def __init__(self, main_grid, area_title, forecast):
        super(OriginatorPersonAddArea, self).__init__(main_grid, area_title, forecast)
        
    def create_list_treeview(self):
        self.originators_person_treestore = Gtk.ListStore(str,str,str)
        self.populate_originators_person_treestore()
        originators_person_treeview = Gtk.TreeView(self.originators_person_treestore)
        originators_person_treeview.append_column(add_column_to_treeview("person_sid", 0, True))
        originators_person_treeview.append_column(add_column_to_treeview("originator_sid", 1, True))

        originators_person_treeview.append_column(add_column_to_treeview("Common name", 2, False))
        originators_person_treeview.set_size_request(200,100)
        return originators_person_treeview
        

    def populate_originators_person_treestore(self):
        self.originators_person_treestore.clear()
        cur=get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        data=(self.forecast.sid,)
        cur.execute("""SELECT 
                        fc_person.sid, fc_person.common_name, fc_originator_person.originator_sid 
                        FROM 
                        fc_forecast_originator, fc_originator_person, fc_person 
                        WHERE
                        fc_forecast_originator.forecast_sid=%s AND 
                        fc_forecast_originator.originator_sid=fc_originator_person.originator_sid AND
                        fc_originator_person.person_sid=fc_person.sid
                        """,data)
        for p in cur.fetchall():
            self.originators_person_treestore.append([ "%s" % p.sid, "%s" % p.originator_sid, p.common_name])
        cur.close()

    
    def populate_combobox_model(self):
        combobox_model=Gtk.ListStore(str,str)
        person_list=Person().get_all()
        for p in person_list:
            combobox_model.append(["%s" % p.sid, p.common_name])
        return combobox_model
    
    
    def search_action(self, widget):
        print("nicht implementiert")


    def add_action(self, widget):
        # read person sid
        (current_person_sid,current_person_common_name)=self.get_active_person()
        # insert originator
        originator=Originator(common_name=current_person_common_name)
        originator.insert()
        # insert forecast_originator
        forecast_originator = ForecastOriginator(forecast_sid=self.forecast.sid, originator_sid=originator.sid)
        forecast_originator.insert()
        # insert originator_person
        originator_person=OriginatorPerson(originator_sid=originator.sid,person_sid=current_person_sid)
        originator_person.insert()
        
        self.show_info_dialog("Add successful")
        self.populate_originators_person_treestore()
        
        
        
    def get_active_person(self):
        tree_iter = self.combobox.get_active_iter()
        if tree_iter!=None:
            model = self.combobox.get_model()
            person_sid = model[tree_iter][:2]
            return person_sid
        else:
            print("please choose a person!")
            
            
    def delete_action(self,widget):
        model,tree_iter = self.list_treeview.get_selection().get_selected()
        (originator_sid)=model.get(tree_iter, 1)
        Originator(originator_sid).delete()
        model.remove(tree_iter)   
        self.show_info_dialog("Delete successful")     
