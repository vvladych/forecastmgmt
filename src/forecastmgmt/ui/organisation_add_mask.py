'''
Created on 03.05.2015

@author: vvladych
'''

from gi.repository import Gtk

from forecastmgmt.model.organisation import Organisation
from forecastmgmt.ui.masterdata_abstract_add_mask import AbstractAddMask


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
        save_button.connect("clicked", self.save_organisation)
        self.attach(save_button,1,row,1,1)

        back_button = Gtk.Button("Back", Gtk.STOCK_GO_BACK)
        back_button.connect("clicked", self.parent_callback_func, self.reset_callback)
        self.attach(back_button,2,row,1,1)
        
        
        
    def load_object(self, organisation_to_load=None):
        if organisation_to_load!=None:
            organisation_to_load.load()
            self.loaded_organisation=organisation_to_load
            self.organisation_uuid_text_entry.set_text(organisation_to_load.organisation_uuid)
            self.common_name_text_entry.set_text(organisation_to_load.common_name)
        else:
            self.loaded_organisation=None
        
            
    def save_organisation(self, widget):
        organisation=self.create_object_from_mask()
        if self.loaded_organisation==None:
            organisation.insert()
        else:                
            if self.loaded_organisation!=None and self.loaded_organisation!=organisation:
                self.loaded_organisation.update(organisation)
                self.loaded_organisation=organisation
                self.show_info_dialog("Organisation updated")
            else:
                self.show_info_dialog("Nothing has changed, nothing to update!")
            
        
        
