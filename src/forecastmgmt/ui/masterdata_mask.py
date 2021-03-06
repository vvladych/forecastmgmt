'''
Created on 14.03.2015

@author: vvladych
'''
from gi.repository import Gtk

from masterdata.person_window import PersonWindow
from masterdata.organisation_window import OrganisationWindow 
from masterdata.publisher_window import PublisherWindow 
from masterdata.fc_object_window import FCObjectWindow 


class MasterdataMask(Gtk.Grid):
    
    def __init__(self, main_window, person=None):
        Gtk.Grid.__init__(self)

        self.main_window=main_window

        # Main working pane: contains left pane with actions and working area pane 
        self.main_working_pane=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_working_pane.set_size_request(200,600)        
        self.add(self.main_working_pane)

        # the left pane: actions
        self.main_left_pane = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_left_pane.set_vexpand(True)

        # the middle pane: working area
        self.main_middle_pane = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_middle_pane.set_vexpand(True)
                       
        self.main_working_pane.pack_start(self.main_left_pane, False, False, 0)
        self.main_working_pane.pack_start(self.main_middle_pane, False, False, 0)
        
        self.create_main_left_pane()
        
    #
    # during init, active==0
    #
    def mask_combo_changed(self, mask_combo):
        if mask_combo.get_active()==0:
            self.set_main_area("person")
        elif mask_combo.get_active()==1:
            self.set_main_area("organisation")
        elif mask_combo.get_active()==2:
            self.set_main_area("publisher")
        elif mask_combo.get_active()==3:
            self.set_main_area("fcobject")
        else:
            print("unimplemented")
        
    # 
    # set main left pane
    # 
    def create_main_left_pane(self):
        self.main_left_pane.pack_start(self.mask_chooser(), False, False, 0)
    
    
    def set_main_area(self, main_area_type="person"):
        self.main_working_pane.remove(self.main_middle_pane)
        self.main_middle_pane = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_working_pane.pack_start(self.main_middle_pane, False, False, 0)

        if main_area_type=="person":
            self.main_middle_pane.pack_start(PersonWindow(self.main_window), False, False, 0)
        elif main_area_type=="organisation":
            self.main_middle_pane.pack_start(OrganisationWindow(self.main_window), False, False, 0)
        elif main_area_type=="publisher":
            self.main_middle_pane.pack_start(PublisherWindow(self.main_window), False, False, 0)
        elif main_area_type=="fcobject":
            self.main_middle_pane.pack_start(FCObjectWindow(self.main_window), False, False, 0)
        else:
            print("unimplemented")
        self.main_working_pane.show_all()
    
    def mask_chooser(self):
        vbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # add empty Label
        vbox.pack_start(Gtk.Label(" "), False, False, 0)
        
        # add mask chooser
        mask_store = Gtk.ListStore(int, str)
        mask_store.append([1, "Person"])
        mask_store.append([2, "Organisation"])
        mask_store.append([3, "Publisher"])
        mask_store.append([4, "Object catalog"])
        
        mask_combo = Gtk.ComboBox.new_with_model_and_entry(mask_store)
        mask_combo.set_entry_text_column(1)
        mask_combo.connect("changed", self.mask_combo_changed)
        mask_combo.set_active(0)
        vbox.pack_start(mask_combo, False, False, 0)
        return vbox
    


