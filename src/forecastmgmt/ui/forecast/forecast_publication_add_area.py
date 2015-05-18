'''
Created on 18.05.2015

@author: vvladych
'''
from forecastmgmt.ui.forecast.forecast_abstract_add_area import AbstractAddArea

from gi.repository import Gtk

from forecastmgmt.ui.ui_tools import add_column_to_treeview
from forecastmgmt.model.publication import Publication

from forecastmgmt.dao.db_connection import get_db_connection
import psycopg2.extras


class PublicationAddArea(AbstractAddArea):
    
    def __init__(self, main_grid, area_title, forecast):
        super(PublicationAddArea, self).__init__(main_grid, area_title, forecast)
        
    def create_list_treeview(self):
        self.publications_treestore = Gtk.ListStore(str,str,str,str,str)
        self.populate_publication_treestore()
        publications_treeview = Gtk.TreeView(self.publications_treestore)
        publications_treeview.append_column(add_column_to_treeview("publisher_sid", 0, True))
        publications_treeview.append_column(add_column_to_treeview("publication_sid", 1, True))
        

        publications_treeview.append_column(add_column_to_treeview("Source", 2, False))
        publications_treeview.append_column(add_column_to_treeview("Date", 3, False))
        publications_treeview.append_column(add_column_to_treeview("Title", 4, False))
        
        
        
        publications_treeview.set_size_request(200,100)
        return publications_treeview
    
    def populate_publication_treestore(self):
        self.publications_treestore.clear()
        cur=get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        data=(self.forecast.sid,)
        #cur.execute("""
        #                """,data)
        #for p in cur.fetchall():
        #    self.publication_treestore.append([ "%s" % p.sid, "%s" % p.originator_sid, p.common_name])
        self.publications_treestore.append(["1", "1", "handelsblatt.de", "01.01.2015", "2015 Prognose Arbeitslosigkeit"])
        cur.close()


    def populate_combobox_model(self):
        return Gtk.ListStore(str,str)
        
    
    
    def search_action(self, widget):
        print("nicht implementiert")
        
        
    def delete_action(self,widget):
        model,tree_iter = self.list_treeview.get_selection().get_selected()
        (publication_sid)=model.get(tree_iter, 1)
        Publication(publication_sid).delete()
        model.remove(tree_iter)   
        self.show_info_dialog("Delete successful")  
