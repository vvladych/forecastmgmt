from gi.repository import Gtk
from forecastmgmt.dao.person_dao import PersonDAO

class PersonListMask(Gtk.Box):

    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.store = Gtk.ListStore(str, str)        
        tree = Gtk.TreeView(self.store)                
        tree.append_column(self.add_column_to_treeview("Vorname", 0))
        tree.append_column(self.add_column_to_treeview("Nachname", 1))
        tree.set_size_request(200,300)
        self.pack_start(tree, False, False, 0)        
        self.populate_person_view_table()
        
    
    def add_column_to_treeview(self, columnname, counter):
        column=Gtk.TreeViewColumn(columnname)
        renderer=Gtk.CellRendererText()
        column.pack_start(renderer, True)
        column.add_attribute(renderer, "text", counter)
        return column
        

    def populate_person_view_table(self):
        persons = PersonDAO().get_all_persons()
        for person in persons:
            self.store.append(["%s" % person.get_sid(), person.get_common_name()])
        
