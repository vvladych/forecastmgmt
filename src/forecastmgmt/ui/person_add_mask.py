
from gi.repository import Gtk
from forecastmgmt.dao.person_dao import PersonDAO

class PersonAddMask(Gtk.Box):
    def __init__(self):
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

