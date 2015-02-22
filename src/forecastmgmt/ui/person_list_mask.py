from gi.repository import Gtk
from forecastmgmt.dao.person_dao import PersonDAO

class PersonListMask(Gtk.Box):

    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.store = Gtk.ListStore(str,str,str,str,bool)        
        tree = Gtk.TreeView(self.store)  
        # add person's common name              
        tree.append_column(self.add_column_to_treeview("common name", 0))
        tree.append_column(self.add_column_to_treeview("birth date", 1))
        tree.append_column(self.add_column_to_treeview("birth place", 2))
        tree.append_column(self.add_column_to_treeview("person uuid", 3))
        
        renderer_toggle=Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_toggled)
        column_toggle=Gtk.TreeViewColumn("delete", renderer_toggle, active=4)
        tree.append_column(column_toggle)
        
        
        tree.set_size_request(200,300)
        self.pack_start(tree, False, False, 0)        
        self.populate_person_view_table()
        
    
    def on_cell_toggled(self,widget,path):
        self.store[path][4]=not self.store[path][4]
        
    
    def add_column_to_treeview(self, columnname, counter):
        column=Gtk.TreeViewColumn(columnname)
        renderer=Gtk.CellRendererText()
        column.pack_start(renderer, True)
        column.add_attribute(renderer, "text", counter)
        return column
        

    def populate_person_view_table(self):
        persons = PersonDAO().get_all_persons()
        for person in persons:
            self.store.append(["%s" % person.common_name, "%s" % person.birth_date, "%s" % person.birth_place, "%s" % person.person_uuid, False])
        
