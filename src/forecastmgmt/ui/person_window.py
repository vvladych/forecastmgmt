from gi.repository import Gtk

from masterdata_abstract_window import MasterdataAbstractWindow

from person_add_mask import PersonAddMask
from person_list_mask import PersonListMask

class PersonWindow(MasterdataAbstractWindow):

    def __init__(self, main_window):
        super(PersonWindow, self).__init__(main_window)
        self.add_working_area(None, "list")

        
    def add_working_area(self, widget, action="list"):
        self.clean_working_area_box()
        self.clean_action_area_box()
        self.create_action_area()
        if action=="list":
            self.personListMask=PersonListMask()
            self.working_area.pack_start(self.personListMask, False, False, 0)
        elif action=="add":
            self.working_area.pack_start(PersonAddMask(self.default_view, self.main_window), False, False, 0)
        elif action=="edit":
            self.working_area.pack_start(PersonAddMask(self.default_view, self.main_window, self.get_current_person()), False, False, 0)

        self.working_area.show_all()   


    def get_current_person(self):
        return self.personListMask.get_current_person()


    def default_view(self):
        self.add_working_area("list")
        
        
    def delete_action(self,widget,callback):
        confirm_dialog=DeletePersonConfirmationDialog(self.main_window)
        response = confirm_dialog.run()
        if response==Gtk.ResponseType.OK:
            self.personListMask.delete_person()
            print("OK")
        elif response==Gtk.ResponseType.CANCEL:
            print("Cancel was clicked")
        confirm_dialog.destroy()
        

        
class DeletePersonConfirmationDialog(Gtk.Dialog):
    
    def __init__(self,parent):
        Gtk.Dialog.__init__(self, "Confirm delete person(s)", parent, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(150, 100)
        label = Gtk.Label("Delete chosen person(s)?")
        box = self.get_content_area()
        box.add(label)
        self.show_all()
        
