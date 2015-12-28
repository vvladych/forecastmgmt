'''
Created on 04.05.2015

@author: vvladych
'''
from gi.repository import Gtk

from src.forecastmgmt.model.fc_object import FCObject
from src.forecastmgmt.ui.masterdata.masterdata_abstract_window import AbstractAddMask

from src.forecastmgmt.ui.ui_tools import add_column_to_treeview


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
        self.attach(self.object_property_treeview,0,row,4,1)

        row+=3
        
        # last row
        save_button = Gtk.Button("Save", Gtk.STOCK_SAVE)
        save_button.connect("clicked", self.save_current_object)
        self.attach(save_button,1,row,1,1)

        back_button = Gtk.Button("Back", Gtk.STOCK_GO_BACK)
        back_button.connect("clicked", self.parent_callback_func, self.reset_callback)
        self.attach(back_button,2,row,1,1)
        


    def create_object_property_treeview(self):
        self.object_property_treestore = Gtk.TreeStore(int,str,str)
        self.object_property_treeview = Gtk.TreeView(self.object_property_treestore)
        self.object_property_treeview.append_column(add_column_to_treeview("property_sid", 0, True))
        self.object_property_treeview.append_column(add_column_to_treeview("property_uuid", 1, True))
        self.object_property_treeview.append_column(add_column_to_treeview("Property", 2, False))
        self.object_property_treeview.set_size_request(200,300)
        self.object_property_treeview.connect("row-activated", self.on_row_selection)
        
        
    def on_row_selection(self,treeview,path,column):
        model,treeiter=self.object_property_treeview.get_selection().get_selected()
        self.object_property_value_entry.set_text(model[treeiter][2])
        

    def add_object_property(self,widget):
        self.object_property_treestore.append(None,[None,None,self.object_property_value_entry.get_text()])
        self.object_property_value_entry.set_text('')



    def delete_object_property(self, widget):
        model,tree_iter = self.object_property_treeview.get_selection().get_selected()
        model.remove(tree_iter)


        
    def fill_mask_from_current_object(self):
        self.object_property_treestore.clear()
        if self.current_object!=None:
            self.uuid_text_entry.set_text(self.current_object.uuid)
            self.common_name_text_entry.set_text(self.current_object.common_name)
            for object_property in self.current_object.object_properties:
                self.object_property_treestore.append(None, [object_property.sid, object_property.uuid, object_property.common_name])
        else:
            self.uuid_text_entry.set_text("")
            self.common_name_text_entry.set_text("")
        
            
        
    def create_object_from_mask(self):
        common_name = self.common_name_text_entry.get_text()
        if common_name is None:
            self.show_error_dialog("common name cannot be null")
            return
        
        fc_object_sid=None
        
        if self.current_object!=None:
            print("current_object is not None")
            fc_object_sid=self.current_object.sid

        
        fc_object=FCObject(fc_object_sid,None,common_name)
                
        # insert object properties
        object_property_iter=self.object_property_treestore.get_iter_first()
        while object_property_iter:
            (object_property_sid, object_property_uuid, object_property_common_name)=self.object_property_treestore.get(object_property_iter, 0, 1, 2)
            
            fc_object.add_object_property(object_property_sid, object_property_uuid, object_property_common_name)
            object_property_iter=self.object_property_treestore.iter_next(object_property_iter)

        return fc_object
    
