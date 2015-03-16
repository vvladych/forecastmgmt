from gi.repository import Gtk
from forecastmgmt.model.person import Person, get_all_persons

from ui_tools import add_column_to_treeview

class PersonListMask(Gtk.Box):

    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.store = Gtk.ListStore(str,str,str,str,str)        
        self.tree = Gtk.TreeView(self.store)  
        # add person's common name              
        self.tree.append_column(add_column_to_treeview("common name", 0, False))
        self.tree.append_column(add_column_to_treeview("birth date", 1, False))
        self.tree.append_column(add_column_to_treeview("birth place", 2, False))
        self.tree.append_column(add_column_to_treeview("person uuid", 3, False))
        self.tree.append_column(add_column_to_treeview("person_sid", 4, True))
        
        self.tree.get_column(0).set_sort_order(Gtk.SortType.ASCENDING)
        self.tree.get_column(0).set_sort_column_id(0)
        
        self.tree.set_size_request(200,300)
        self.pack_start(self.tree, False, False, 0)        
        self.populate_person_view_table()
        
        

    def populate_person_view_table(self):
        persons = get_all_persons()
        for person in persons:
            self.store.append(["%s" % person.common_name, "%s" % person.birth_date, "%s" % person.birth_place, "%s" % person.person_uuid, "%s" % person.sid])
        

    def delete_person(self):
        model,tree_iter = self.tree.get_selection().get_selected()
        (person_sid)=self.store.get(tree_iter, 4)
        Person(person_sid).delete()
        self.store.remove(tree_iter)
            
    def get_current_person(self):
        model,tree_iter = self.tree.get_selection().get_selected()
        (person_sid)=self.store.get(tree_iter, 4)
        return Person(person_sid)
