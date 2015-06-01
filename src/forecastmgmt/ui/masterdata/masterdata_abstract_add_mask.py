'''
Created on 03.05.2015

@author: vvladych
'''

from gi.repository import Gtk

class AbstractAddMask(Gtk.Grid):
    def __init__(self, main_window, reset_callback=None):
        Gtk.Grid.__init__(self)
        self.main_window=main_window
        self.reset_callback=reset_callback
        self.create_layout()
        self.current_object=None        
        
        
    def set_masterdata_object(self, masterdata_object=None):
        self.masterdata_object=masterdata_object
        self.load_object(masterdata_object)
                
    
    def create_layout(self):
        raise NotImplementedError("create_layout not implemented!")
    
    def create_object_from_mask(self):    
        raise NotImplementedError("create_object_from_mask not implemented!")
        
        
    def show_info_dialog(self, message):
        info_dialog = Gtk.MessageDialog(self.main_window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, message)
        info_dialog.run()
        info_dialog.destroy()
        

    def show_error_dialog(self, message):
        error_dialog = Gtk.MessageDialog(self.main_window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, message)
        error_dialog.run()
        error_dialog.destroy()
        
        
    def parent_callback_func(self, widget, cb_func=None):
        self.reset_callback()
        
    def save_current_object(self, widget):
        new_object=self.create_object_from_mask()
        if self.current_object==None:
            new_object.insert()
            self.show_info_dialog("Insert successful")
            self.current_object=new_object
            self.reset_callback()
        else:
            if self.current_object!=new_object:
                self.current_object.update(new_object)
                self.loaded_organisation=new_object
                self.show_info_dialog("Update successful")
            else:
                self.show_info_dialog("Nothing has changed, nothing to update!")
                
        
    def load_object(self, object_to_load=None):
        self.current_object=object_to_load
        if object_to_load!=None:
            object_to_load.load()
        self.fill_mask_from_current_object()
            
            
        

