'''
Created on 04.05.2015

@author: vvladych
'''
from gi.repository import Gtk

from forecastmgmt.model.fc_object import FCObject
from masterdata_abstract_window import AbstractAddMask


class FCObjectAddMask(AbstractAddMask):
    def __init__(self, main_window, reset_callback):
        super(FCObjectAddMask, self).__init__(main_window, reset_callback)


    def create_layout(self):
        self.set_column_spacing(5)
        self.set_row_spacing(3)

        placeholder_label = Gtk.Label("")
        placeholder_label.set_size_request(1,40)
        self.attach(placeholder_label,0,-1,1,1)

        row = 0
        self.add_uuid_row("Object UUID", row)
         
        row+=1
        self.add_common_name_row("Common name", row)

        row+=3
        # Object property
        object_property_label = Gtk.Label("Object properties")
        self.attach(object_property_label,0,row,1,1)

        object_property_add_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        object_property_add_button.connect("clicked", self.add_object_property) 
        self.attach(object_property_add_button,2,row,1,1)

        object_property_delete_button = Gtk.Button("Delete", Gtk.STOCK_DELETE)
        object_property_delete_button.connect("clicked", self.delete_object_property) 
        self.attach(object_property_delete_button,3,row,1,1)

        self.object_property_value_entry = Gtk.Entry()
        self.attach(self.object_property_value_entry,1,row,1,1)

        row+=1
        self.create_object_property_treeview()
        self.attach(self.object_property_treeview,0,row,1,1)

        row+=3
        
        # last row
        save_button = Gtk.Button("Save", Gtk.STOCK_SAVE)
        save_button.connect("clicked", self.save_current_object)
        self.attach(save_button,1,row,1,1)

        back_button = Gtk.Button("Back", Gtk.STOCK_GO_BACK)
        back_button.connect("clicked", self.parent_callback_func, self.reset_callback)
        self.attach(back_button,2,row,1,1)
        
    def add_object_property(self, widget):
        print("not implemented")


    def delete_object_property(self, widget):
        print("not implemented")

    def create_object_property_treeview(self):
        self.object_property_treeview=Gtk.TreeView()
        print("not implemented")

        
    def fill_mask_from_current_object(self):
        if self.current_object!=None:
            self.uuid_text_entry.set_text(self.current_object.uuid)
            self.common_name_text_entry.set_text(self.current_object.common_name)
        else:
            self.uuid_text_entry.set_text("")
            self.common_name_text_entry.set_text("")
        
            
        
    def create_object_from_mask(self):
        common_name = self.common_name_text_entry.get_text()
        if common_name is None:
            self.show_error_dialog("common name cannot be null")
            return
        fc_object=FCObject(None,common_name)
        return fc_object
    
