from gi.repository import Gtk
from forecastmgmt.dao.person_dao import PersonDAO

from person_edit_mask import PersonEditMask
from person_add_mask import PersonAddMask
from person_list_mask import PersonListMask

class PersonWindow(Gtk.Box):

    def __init__(self, main_window):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.main_window=main_window
        self.person_action_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.pack_start(self.person_action_area, False, False, 0)
        self.person_working_area=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.pack_start(self.person_working_area, False, False, 0)
        
        self.add_working_area(None, "list")

    def create_action_area(self, action="list"):
        if action=="list":
            self.add_new_person_button=Gtk.Button.new_from_stock(Gtk.STOCK_ADD)
            self.add_new_person_button.set_size_request(30,30)
            self.add_new_person_button.connect("clicked", self.add_working_area, "add")
            self.person_action_area.pack_start(self.add_new_person_button, False, False, 0)
        elif action=="add":
            save_new_person=Gtk.Button.new_from_stock(Gtk.STOCK_SAVE)
            self.person_action_area.pack_start(save_new_person, False, False, 0)
            cancel_new_person=Gtk.Button.new_from_stock(Gtk.STOCK_CANCEL)
            cancel_new_person.connect("clicked", self.add_working_area, "list")
            self.person_action_area.pack_start(cancel_new_person, False, False, 0)

        self.person_action_area.show_all()

    def clean_working_area_box(self):
        for child in self.person_working_area.get_children():
            self.person_working_area.remove(child)

    def clean_action_area_box(self):
        for child in self.person_action_area.get_children():
            self.person_action_area.remove(child)

    def add_working_area(self, widget, action="list"):
        self.clean_working_area_box()
        self.clean_action_area_box()
        self.create_action_area(action)
        if action=="list":
            self.person_working_area.pack_start(PersonListMask(), False, False, 0)
        elif action=="add":
            self.person_working_area.pack_start(PersonAddMask(self.default_view, self.main_window), False, False, 0)
        self.person_working_area.show_all()

    def default_view(self):
        self.add_working_area("list")
        

    def reset_callback(self):
        print("in reset_callback person_window")
