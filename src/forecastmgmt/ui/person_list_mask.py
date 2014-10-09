from gi.repository import Gtk
from forecastmgmt.dao.person_dao import PersonDAO

class PersonListMask():

    def __init__(self):
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox.pack_start(self.create_header_bar(), False, False, 0)        
        self.vbox.pack_start(self.add_person_view_table(), False, False, 0)
        
        
    def get_view(self):
        return self.vbox
        
        
    def add_person_view_table(self):
        self.store = Gtk.ListStore(str, str)
        self.populate_person_view_table()
        
        tree = Gtk.TreeView(self.store)
                
        tree.append_column(self.add_column_to_treeview("Vorname", 0))
        tree.append_column(self.add_column_to_treeview("Nachname", 1))
        tree.set_size_request(200,300)
        return tree
        
        
    def populate_person_view_table(self):
        persons = PersonDAO().get_all_persons()
        for person in persons:
            self.store.append(["%s" % person.get_sid(), person.get_common_name()])

        
    
    def add_column_to_treeview(self, columnname, counter):
        column=Gtk.TreeViewColumn(columnname)
        renderer=Gtk.CellRendererText()
        column.pack_start(renderer, True)
        column.add_attribute(renderer, "text", counter)
        return column
        
    def create_header_bar(self):
        halign = Gtk.Alignment()
        halign.set(0,1,0,0)
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(False)
        box=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box.set_spacing(10)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")
        
        add_new_person_button=Gtk.Button.new_from_stock(Gtk.STOCK_ADD)
        add_new_person_button.set_size_request(30,30)
        box.add(add_new_person_button)
        
        delete_person_button=Gtk.Button.new_from_stock(Gtk.STOCK_DELETE)
        box.add(delete_person_button)        
        
        hb.pack_start(box)
        
        halign.add(hb)
        return halign        
