from gi.repository import Gtk

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

            self.edit_person_button=Gtk.Button.new_from_stock(Gtk.STOCK_EDIT)
            self.edit_person_button.set_size_request(30,30)
            self.edit_person_button.connect("clicked", self.add_working_area, "edit")
            self.person_action_area.pack_start(self.edit_person_button, False, False, 0)

            
            self.delete_person_button=Gtk.Button.new_from_stock(Gtk.STOCK_DELETE)
            self.delete_person_button.set_size_request(30,30)
            self.delete_person_button.connect("clicked", self.delete_person, "delete")
            self.person_action_area.pack_start(self.delete_person_button, False, False, 0)

        self.person_action_area.show_all()
        
            

    def clean_action_area_box(self):
        for child in self.person_action_area.get_children():
            self.person_action_area.remove(child)
            

    def add_working_area(self, widget, action="list"):
        self.clean_working_area_box()
        self.clean_action_area_box()
        self.create_action_area(action)
        if action=="list":
            self.personListMask=PersonListMask()
            self.person_working_area.pack_start(self.personListMask, False, False, 0)
        elif action=="add":
            self.person_working_area.pack_start(PersonAddMask(self.default_view, self.main_window), False, False, 0)
        elif action=="edit":
            person=self.get_current_person()
            self.person_working_area.pack_start(PersonAddMask(self.default_view, self.main_window, person), False, False, 0)

        self.person_working_area.show_all()

    def get_current_person(self):
        person=self.personListMask.get_current_person()
        return person
            


    def clean_working_area_box(self):
        for child in self.person_working_area.get_children():
            self.person_working_area.remove(child)


    def default_view(self):
        self.add_working_area("list")
        
        
    def delete_person(self,widget,callback):
        confirm_dialog=DeletePersonConfirmationDialog(self.main_window)
        response = confirm_dialog.run()
        if response==Gtk.ResponseType.OK:
            self.personListMask.delete_person()
            print("OK")
        elif response==Gtk.ResponseType.CANCEL:
            print("Cancel was clicked")
        confirm_dialog.destroy()
        

    def reset_callback(self):
        print("in reset_callback person_window")
        
class DeletePersonConfirmationDialog(Gtk.Dialog):
    
    def __init__(self,parent):
        Gtk.Dialog.__init__(self, "Confirm delete person(s)", parent, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(150, 100)
        label = Gtk.Label("Delete chosen person(s)?")
        box = self.get_content_area()
        box.add(label)
        self.show_all()
        
