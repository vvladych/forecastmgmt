'''
Created on 04.05.2015

@author: vvladych
'''
from gi.repository import Gtk

from forecastmgmt.model.publisher import Publisher
from forecastmgmt.ui.masterdata.object_add_mask.masterdata_abstract_add_mask import AbstractAddMask


class PublisherAddMask(AbstractAddMask):
    def __init__(self, main_window, reset_callback):
        super(PublisherAddMask, self).__init__(main_window, reset_callback)
        self.loaded_publisher=None


    def create_layout(self):
        self.set_column_spacing(5)
        self.set_row_spacing(3)

        placeholder_label = Gtk.Label("")
        placeholder_label.set_size_request(1,40)
        self.attach(placeholder_label,0,-1,1,1)

        row = 0
        # Row 0: publisher uuid
        uuid_label = Gtk.Label("publisher UUID")
        uuid_label.set_justify(Gtk.Justification.LEFT)
        self.attach(uuid_label,0,row,1,1)
        self.publisher_uuid_text_entry=Gtk.Entry()
        self.publisher_uuid_text_entry.set_editable(False)
        self.attach(self.publisher_uuid_text_entry,1,row,1,1)
        
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
        save_button.connect("clicked", self.save_publisher)
        self.attach(save_button,1,row,1,1)

        back_button = Gtk.Button("Back", Gtk.STOCK_GO_BACK)
        back_button.connect("clicked", self.parent_callback_func, self.reset_callback)
        self.attach(back_button,2,row,1,1)
        
        
        
    def load_object(self, publisher_to_load=None):
        if publisher_to_load!=None:
            publisher_to_load.load()
            self.loaded_publisher=publisher_to_load
            self.publisher_uuid_text_entry.set_text(publisher_to_load.publisher_uuid)
            self.common_name_text_entry.set_text(publisher_to_load.common_name)
        else:
            self.publisher_to_load=None
            self.publisher_uuid_text_entry.set_text("")
            self.common_name_text_entry.set_text("")
        
            
    def save_publisher(self, widget):
        publisher=self.create_object_from_mask()
        if self.loaded_publisher==None:
            publisher.insert()
            self.show_info_dialog("Publisher successful inserted")
            self.loaded_publisher=publisher
            self.reset_callback()
        else:                
            if self.loaded_publisher!=None and self.loaded_publisher!=publisher:
                self.loaded_publisher.update(publisher)
                self.loaded_publisher=publisher
                self.show_info_dialog("Publisher updated")
            else:
                self.show_info_dialog("Nothing has changed, nothing to update!")
            
        
    def create_object_from_mask(self):
        common_name = self.common_name_text_entry.get_text()
        if common_name is None:
            self.show_error_dialog("common name cannot be null")
            return
        publisher=Publisher(None,common_name)
        return publisher
    
