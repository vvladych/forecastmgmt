'''
Created on 14.03.2015

@author: vvladych
'''
from gi.repository import Gtk

from forecastmgmt.ui.person_window import PersonWindow 

class MasterdataMask(Gtk.Grid):
    
    def __init__(self, main_window, person=None):
        Gtk.Grid.__init__(self)

        self.main_window=main_window

        # Main working pane: contains left pane with actions and working area pane 
        self.main_working_pane=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(self.main_working_pane)

        # the left pane: actions
        self.main_left_pane = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        # the middle pane: working area
        self.main_middle_pane = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
                       
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
        else:
            print("unimplemented")
        
    # 
    # set main left pane
    # 
    def create_main_left_pane(self):
        self.main_left_pane.pack_start(self.mask_chooser(), False, False, 0)
    
    
    def set_main_area(self, main_area_type="person"):
        if main_area_type=="person":
            self.main_middle_pane.pack_start(PersonWindow(self), False, False, 0)
        #elif main_area_type=="organization":
        #    self.main_middle_pane.pack_start(OrganisationMask(), False, False, 0)
        else:
            print("unimplemented")
    
    def mask_chooser(self):
        vbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # add empty Label
        vbox.pack_start(Gtk.Label(" "), False, False, 0)
        
        # add mask chooser
        mask_store = Gtk.ListStore(int, str)
        mask_store.append([1, "Person"])
        mask_store.append([2, "Organisation"])
        mask_combo = Gtk.ComboBox.new_with_model_and_entry(mask_store)
        mask_combo.set_entry_text_column(1)
        mask_combo.connect("changed", self.mask_combo_changed)
        mask_combo.set_active(0)
        vbox.pack_start(mask_combo, False, False, 0)
        return vbox
    

