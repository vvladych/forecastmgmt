'''
Created on 16.05.2015

@author: vvladych
'''

from gi.repository import Gtk


class AbstractAddArea(object):
    
    def __init__(self, maingrid, area_title, forecast):
        self.maingrid=maingrid
        self.area_title=area_title
        self.forecast=forecast
        
    
    def create_layout(self, row):
        
        self.originator_label = Gtk.Label(self.area_title)
        self.originator_label.set_justify(Gtk.Justification.LEFT)
        self.maingrid.attach(self.originator_label,0,row,1,1)
        
        self.combobox_model=self.populate_combobox_model()
        self.combobox=Gtk.ComboBox.new_with_model_and_entry(self.combobox_model)
        self.combobox.set_entry_text_column(1)
        self.maingrid.attach(self.combobox,1,row,1,1)
        
        self.or_search_label = Gtk.Label("OR")
        self.or_search_label.set_justify(Gtk.Justification.LEFT)
        self.maingrid.attach(self.or_search_label,2,row,1,1)

        self.search_button = Gtk.Button("Search", Gtk.STOCK_FIND)
        self.search_button.connect("clicked", self.search_action) 
        self.maingrid.attach(self.search_button,3,row,1,1)

                
        row += 1
        self.add_button=Gtk.Button("Add", Gtk.STOCK_ADD)
        self.maingrid.attach(self.add_button,1,row,1,1)
        self.add_button.connect("clicked", self.add_action)
        
        self.delete_button=Gtk.Button("Delete", Gtk.STOCK_DELETE)
        self.delete_button.connect("clicked", self.delete_action)        
        self.maingrid.attach(self.delete_button,2,row,1,1)

        row += 1
        self.list_treeview=self.create_list_treeview()
        self.maingrid.attach(self.list_treeview,0,row,2,1)
        
        return row


    def populate_combobox_model(self):
        raise NotImplementedError("Still not implemented!")
        
    def search_action(self, widget):
        raise NotImplementedError("Still not implemented")
        
    def add_action(self, widget):
        raise NotImplementedError("Still not implemented")
            
    def delete_action(self, widget):
        raise NotImplementedError("Still not implemented")
            
            
    def create_list_treeview(self):
        raise NotImplementedError("Still not implemented")
        
    

    def show_info_dialog(self, message):
        info_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, message)
        info_dialog.run()
        info_dialog.destroy()
