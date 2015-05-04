'''
Created on 27.04.2015

@author: vvladych
'''

from gi.repository import Gtk


class  MasterdataAbstractWindow(Gtk.Box):
    
    def __init__(self, main_window, listmask, addmask):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.main_window=main_window
        self.listmask=listmask
        self.addmask=addmask
        
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
        confirm_dialog=DeleteConfirmationDialog(self.main_window)
        response = confirm_dialog.run()
        if response==Gtk.ResponseType.OK:
            self.listmask.delete_object()
            print("OK")
        elif response==Gtk.ResponseType.CANCEL:
            print("Cancel was clicked")
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
    
    
class DeleteConfirmationDialog(Gtk.Dialog):
    
    def __init__(self,parent,object_name=None):
        Gtk.Dialog.__init__(self, "Confirm delete %s(s)" % object_name, parent, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(150, 100)
        label = Gtk.Label("Delete chosen %s(s)?" % object_name)
        box = self.get_content_area()
        box.add(label)
        self.show_all()

    


