from gi.repository import Gtk
from forecastmgmt.dao.person_dao import PersonDAO
from forecastmgmt.model.person import Person

from ui_tools import add_column_to_treeview

class PersonListMask(Gtk.Box):

    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.store = Gtk.ListStore(str,str,str,str,bool,str)        
        tree = Gtk.TreeView(self.store)  
        # add person's common name              
        tree.append_column(add_column_to_treeview("common name", 0, False))
        tree.append_column(add_column_to_treeview("birth date", 1, False))
        tree.append_column(add_column_to_treeview("birth place", 2, False))
        tree.append_column(add_column_to_treeview("person uuid", 3, False))
        
        
        renderer_toggle=Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_toggled)
        column_toggle=Gtk.TreeViewColumn("delete", renderer_toggle, active=4)
        tree.append_column(column_toggle)
        
        tree.append_column(add_column_to_treeview("person_sid", 5, True))
        
        
        tree.set_size_request(200,300)
        self.pack_start(tree, False, False, 0)        
        self.populate_person_view_table()
        
    
    def on_cell_toggled(self,widget,path):
        self.store[path][4]=not self.store[path][4]
        

    def populate_person_view_table(self):
        persons = PersonDAO().get_all_persons()
        for person in persons:
            self.store.append(["%s" % person.common_name, "%s" % person.birth_date, "%s" % person.birth_place, "%s" % person.person_uuid, False, "%s" % person.sid])
        

    def delete_person(self):
        # get chosen persons
        iter=self.store.get_iter_first()
        while iter:
            (person_sid)=self.store.get(iter, 5)
            flag_to_delete="%s" % self.store.get(iter,4)
            
            if flag_to_delete=="True":
                print("loesche: %s" % person_sid)
                PersonDAO().delete(Person(person_sid))
                self.store.remove(iter)
            iter=self.store.iter_next(iter)
