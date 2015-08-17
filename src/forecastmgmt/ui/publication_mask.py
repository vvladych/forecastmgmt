from gi.repository import Gtk

from abstract_mask import AbstractMask
from ui_tools import add_column_to_treeview, show_info_dialog
from forecastmgmt.model.publication import Publication



class PublicationMask(AbstractMask):
    
    def __init__(self, main_window):
        super(PublicationMask, self).__init__(main_window)

    def create_overview_treeview(self):
        self.publications_treestore = Gtk.TreeStore(int,str,str,str)
        self.__populate_publications_treestore()
        self.overview_treeview = Gtk.TreeView(self.publications_treestore)
        self.overview_treeview.append_column(add_column_to_treeview("id", 0, True))
        self.overview_treeview.append_column(add_column_to_treeview("Publisher", 1, False))
        self.overview_treeview.append_column(add_column_to_treeview("Date", 2, False))
        self.overview_treeview.append_column(add_column_to_treeview("Title", 3, False))
        
    def __populate_publications_treestore(self):
        self.publications_treestore.clear()
        for publication in Publication().get_all():
            self.publications_treestore.append(None,[publication.sid,"","%s" % publication.publishing_date,publication.title])
            
            
    def add_context_menu_overview_treeview(self):
        menu=Gtk.Menu()
        menu_item_create_new_publication=Gtk.MenuItem("Add new publication...")
        #menu_item_create_new_forecast.connect("activate", self.on_menu_item_create_new_forecast_click) 
        menu.append(menu_item_create_new_publication)
        menu_item_create_new_publication.show()
        menu_item_delete_publication=Gtk.MenuItem("Delete publication...")
        #menu_item_delete_publication.connect("activate", self.on_menu_item_delete_forecast_click) 
        menu.append(menu_item_delete_publication)
        menu_item_delete_publication.show()
        #self.overview_treeview.connect("button_press_event", self.on_treeview_button_press_event,menu)
