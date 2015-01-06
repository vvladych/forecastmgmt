
from gi.repository import Gtk
from forecastmgmt.dao.person_dao import PersonDAO

class PersonAddMask(Gtk.Box):
    def __init__(self, reset_callback):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        #layout_table = Gtk.Table(2,2,True)
        #common_name_label = Gtk.Label("Common name")
        #self.common_name_entry = Gtk.Entry()
        uuid_label = Gtk.Label("person UUID")
        #self.uuid_entry_label = Gtk.Label()
        #layout_table.attach(common_name_label, 0,1,0,1)
        #layout_table.attach(self.common_name_entry, 1,2,0,1)
        #layout_table.attach(uuid_label, 1,2,0,1)
        #layout_table.attach(self.uuid_entry_label, 1,2,1,2)
        self.pack_start(uuid_label, False, False, 0)
        test_button = Gtk.Button("Test", Gtk.STOCK_OK)
        test_button.connect("clicked", self.parent_callback_func, reset_callback)
        self.pack_start(test_button, False, False, 0)

    def parent_callback_func(self, widget, cb_func=None):
        print("in reset_callback")
        cb_func()
