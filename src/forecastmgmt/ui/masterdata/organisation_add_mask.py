'''
Created on 03.05.2015

@author: vvladych
'''

from gi.repository import Gtk

from forecastmgmt.model.organisation import Organisation
from forecastmgmt.ui.masterdata.object_add_mask.masterdata_abstract_add_mask import AbstractAddMask


class OrganisationAddMask(AbstractAddMask):
    def __init__(self, main_window, reset_callback):
        super(OrganisationAddMask, self).__init__(main_window, reset_callback)


    def create_layout(self):
        self.set_column_spacing(5)
        self.set_row_spacing(3)

        placeholder_label = Gtk.Label("")
        placeholder_label.set_size_request(1,40)
        self.attach(placeholder_label,0,-1,1,1)

        row = 0
        # Row 0: organisation uuid
        uuid_label = Gtk.Label("organisation UUID")
        uuid_label.set_justify(Gtk.Justification.LEFT)
        self.attach(uuid_label,0,row,1,1)
        self.organisation_uuid_text_entry=Gtk.Entry()
        self.organisation_uuid_text_entry.set_editable(False)
        self.attach(self.organisation_uuid_text_entry,1,row,1,1)
        
        row+=1
        # Row 1: common name
        common_name_label = Gtk.Label("Common Name")
        common_name_label.set_justify(Gtk.Justification.LEFT)
        self.attach(common_name_label,0,row,1,1)
        self.common_name_text_entry=Gtk.Entry()
        self.attach(self.common_name_text_entry,1,row,1,1)

        row+=1
        
        # last row
        save_button = Gtk.Button("Save", Gtk.STOCK_SAVE)
        save_button.connect("clicked", self.save_current_object)
        self.attach(save_button,1,row,1,1)

        back_button = Gtk.Button("Back", Gtk.STOCK_GO_BACK)
        back_button.connect("clicked", self.parent_callback_func, self.reset_callback)
        self.attach(back_button,2,row,1,1)
                    
        
    def fill_mask_from_current_object(self):
        if self.current_object!=None:
            self.organisation_uuid_text_entry.set_text(self.current_object.uuid)
            self.common_name_text_entry.set_text(self.current_object.common_name)
        else:
            self.organisation_uuid_text_entry.set_text("")
            self.common_name_text_entry.set_text("")
            
            
        
    def create_object_from_mask(self):
        common_name = self.common_name_text_entry.get_text()
        if common_name is None:
            self.show_error_dialog("common name cannot be null")
            return
        organisation=Organisation(None,common_name)
        return organisation
    
