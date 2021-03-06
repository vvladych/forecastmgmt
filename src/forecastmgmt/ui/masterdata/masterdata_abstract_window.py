'''
Created on 27.04.2015

@author: vvladych
'''

from gi.repository import Gtk

from forecastmgmt.ui.ui_tools import add_column_to_treeview

class  MasterdataAbstractWindow(Gtk.Box):
    
    def __init__(self, main_window, listmask, addmask):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.main_window=main_window
        self.listmask=listmask
        self.addmask=addmask
        self.specific_name="unspecified"
        
        self.action_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.pack_start(self.action_area, False, False, 0)

        self.working_area=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.pack_start(self.working_area, False, False, 0)

        self.add_action_area_box()
        self.add_working_area()
        

        
    def reset_working_area(self):
        for child in self.working_area.get_children():
            self.working_area.remove(child)
        

            
    def add_action_area_box(self):
        self.add_new_button=Gtk.Button.new_from_stock(Gtk.STOCK_ADD)
        self.add_new_button.set_size_request(30,30)
        self.add_new_button.connect("clicked", self.add_action)
        self.action_area.pack_start(self.add_new_button, False, False, 0)

        self.edit_button=Gtk.Button.new_from_stock(Gtk.STOCK_EDIT)
        self.edit_button.set_size_request(30,30)
        self.edit_button.connect("clicked", self.edit_action, "edit")
        self.action_area.pack_start(self.edit_button, False, False, 0)

        
        self.delete_button=Gtk.Button.new_from_stock(Gtk.STOCK_DELETE)
        self.delete_button.set_size_request(30,30)
        self.delete_button.connect("clicked", self.delete_action, "delete")
        self.action_area.pack_start(self.delete_button, False, False, 0)

        self.action_area.show_all()
        
    def delete_action(self,widget,callback):
        confirm_dialog=DeleteConfirmationDialog(self.main_window, self.specific_name)
        response = confirm_dialog.run()
        if response==Gtk.ResponseType.OK:
            self.listmask.delete_object()
            self.show_info_dialog("Delete successful")
        elif response==Gtk.ResponseType.CANCEL:
            self.show_info_dialog("Delete canceled")
        confirm_dialog.destroy()
    
    
    def add_action(self,widget,callback=None):
        self.reset_working_area()
        self.addmask.load_object(None)
        self.working_area.pack_start(self.addmask, False, False, 0)
        self.working_area.show_all()   
        
    
    def edit_action(self,widget,callback):
        self.reset_working_area()
        self.addmask.set_masterdata_object(self.listmask.get_current_object())
        self.working_area.pack_start(self.addmask, False, False, 0)
        self.working_area.show_all()
    

    
    def add_working_area(self):
        self.reset_working_area()
        self.listmask.populate_object_view_table()
        self.working_area.pack_start(self.listmask, False, False, 0)
        self.working_area.show_all()   
        
    def show_info_dialog(self, message):
        info_dialog = Gtk.MessageDialog(self.main_window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, message)
        info_dialog.run()
        info_dialog.destroy()
        

    def show_error_dialog(self, message):
        error_dialog = Gtk.MessageDialog(self.main_window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, message)
        error_dialog.run()
        error_dialog.destroy()
        
    
    
class DeleteConfirmationDialog(Gtk.Dialog):
    
    def __init__(self,parent,object_name=None):
        Gtk.Dialog.__init__(self, "Confirm delete %s(s)" % object_name, parent, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(150, 100)
        label = Gtk.Label("Delete chosen %s(s)?" % object_name)
        box = self.get_content_area()
        box.add(label)
        self.show_all()


class AbstractAddMask(Gtk.Grid):
    def __init__(self, main_window, reset_callback=None):
        Gtk.Grid.__init__(self)
        self.main_window=main_window
        self.reset_callback=reset_callback
        self.create_layout()
        self.current_object=None        
        
    def add_uuid_row(self, label, row):
        uuid_label = Gtk.Label(label)
        uuid_label.set_justify(Gtk.Justification.LEFT)
        self.attach(uuid_label,0,row,1,1)
        self.uuid_text_entry=Gtk.Entry()
        self.uuid_text_entry.set_editable(False)
        self.attach(self.uuid_text_entry,1,row,1,1)
        

    def add_common_name_row(self, label, row):
        common_name_label = Gtk.Label(label)
        common_name_label.set_justify(Gtk.Justification.LEFT)
        self.attach(common_name_label,0,row,1,1)
        self.common_name_text_entry=Gtk.Entry()
        self.attach(self.common_name_text_entry,1,row,1,1)
        
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
            

class AbstractListMask(Gtk.Box):

    def __init__(self, columnlist):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.store=Gtk.ListStore(*([str]*len(columnlist)))        
        self.tree = Gtk.TreeView(self.store)          
        
        column_counter=0
        for column in columnlist:
            self.tree.append_column(add_column_to_treeview(column["column"], column_counter, column["hide"]))
            column_counter+=1
                    
        self.tree.get_column(0).set_sort_order(Gtk.SortType.ASCENDING)
        self.tree.get_column(0).set_sort_column_id(0)

        self.tree.connect("row-activated", self.on_row_select)
        
        self.tree.set_size_request(200,300)
        self.pack_start(self.tree, False, False, 0)        

        self.populate_object_view_table()
        
        

    def populate_object_view_table(self):
        raise "populate_object_view_table still unimplemented!"
    

    def delete_object(self):
        raise "delete_object still unimplemented!"
    
    def get_current_object(self):
        raise "get_current_object still unimplemented!"
    

    def on_row_select(self,widget,path,data):
        raise NotImplementedError("on_row_select still not implemented!")
        
