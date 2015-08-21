from gi.repository import Gtk

from abstract_mask import AbstractMask
from ui_tools import add_column_to_treeview, show_info_dialog
from forecastmgmt.model.publication import Publication
from forecastmgmt.ui.publication.publication_overview_window import PublicationOverviewWindow



class PublicationMask(AbstractMask):
    
    def __init__(self, main_window):
        super(PublicationMask, self).__init__(main_window)

    def create_overview_treeview(self):
        self.publications_treestore = Gtk.TreeStore(int,str,str,str)
        self.populate_publications_treestore()
        self.overview_treeview = Gtk.TreeView(self.publications_treestore)
        self.overview_treeview.append_column(add_column_to_treeview("id", 0, True))
        self.overview_treeview.append_column(add_column_to_treeview("Publisher", 1, False))
        self.overview_treeview.append_column(add_column_to_treeview("Date", 2, False))
        self.overview_treeview.append_column(add_column_to_treeview("Title", 3, False))
        
    def populate_publications_treestore(self):
        self.publications_treestore.clear()
        for publication in Publication().get_all():
            self.publications_treestore.append(None,[publication.sid,"","%s" % publication.publishing_date,publication.title])
            
            
    def add_context_menu_overview_treeview(self):
        menu=Gtk.Menu()
        menu_item_create_new_publication=Gtk.MenuItem("Add new publication...")
        menu_item_create_new_publication.connect("activate", self.on_menu_item_create_new_publication_click) 
        menu.append(menu_item_create_new_publication)
        menu_item_create_new_publication.show()
        menu_item_delete_publication=Gtk.MenuItem("Delete publication...")
        menu_item_delete_publication.connect("activate", self.on_menu_item_delete_publication_click) 
        menu.append(menu_item_delete_publication)
        menu_item_delete_publication.show()
        self.overview_treeview.connect("button_press_event", self.on_treeview_button_press_event,menu)
        
        
    def on_menu_item_create_new_publication_click(self,widget):
        self.publication=None
        self.clear_main_middle_pane()
        self.main_middle_pane.pack_start(PublicationOverviewWindow(self, publication=None, callback=self.populate_publications_treestore), False, False, 0)
        self.main_middle_pane.show_all()
        
        
    def on_menu_item_delete_publication_click(self,widget):
        self.publication.delete()
        self.publication=None
        self.clear_main_middle_pane()
        show_info_dialog("Publication deleted")
        self.populate_publications_treestore()
        
        
        
    def on_treeview_button_press_event(self,treeview,event,widget):
        x = int(event.x)
        y = int(event.y)
        pthinfo=treeview.get_path_at_pos(x,y)
        if event.button==1:
            if pthinfo is not None:
                treeview.get_selection().select_path(pthinfo[0])    
                publication_sid=self.publications_treestore.get(self.publications_treestore.get_iter(pthinfo[0]),0)
                self.publication=Publication(publication_sid)
                self.publication.load()
                self.clear_main_middle_pane()
                self.main_middle_pane.pack_start(PublicationOverviewWindow(self,self.publication), False, False, 0)
                self.main_middle_pane.show_all()
        
        if event.button==3:
            if pthinfo is not None:
                treeview.get_selection().select_path(pthinfo[0])    
            widget.popup(None, None, None, None, event.button, event.time)    
        return True
