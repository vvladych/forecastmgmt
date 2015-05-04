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
        
        
    def set_masterdata_object(self, masterdata_object=None):
        self.masterdata_object=masterdata_object
        self.load_object(masterdata_object)
                

    def load_object(self,masterdata_object=None):
        raise NotImplementedError("load_object not implemented!")
    
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

