'''
Created on 31.08.2015

@author: vvladych
'''
from gi.repository import Gtk

from forecastmgmt.model.personrole import Personrole
from forecastmgmt.ui.forecast.abstract_data_process_component import AbstractDataOverviewComponent

from forecastmgmt.ui.ui_tools import TreeviewColumn, show_info_dialog


class PersonroleAddDialog(Gtk.Dialog):
    def __init__(self, main_window, reset_callback):
        Gtk.Dialog.__init__(self, "Personrole Dialog", None, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.reset_callback=reset_callback
        self.set_default_size(400, 400)
        self.layout_grid=Gtk.Grid()
        self.create_layout()
        self.show_all()
        


    def create_layout(self):
        box = self.get_content_area()
        
        box.add(self.layout_grid)
        
        
        self.layout_grid.set_column_spacing(5)
        self.layout_grid.set_row_spacing(3)

        placeholder_label = Gtk.Label("")
        placeholder_label.set_size_request(1,40)
        self.layout_grid.attach(placeholder_label,0,-1,1,1)

        row = 0
        # Row 0:  uuid
        self.add_uuid_row("UUID", row)
        
        row+=1
        # Row 1: common name
        self.add_common_name_row("Common Name", row)
        
        row+=1
        
        # last row
        add_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        add_button.connect("clicked", self.add_current_object)
        self.layout_grid.attach(add_button,1,row,1,1)
        
        row+=1
        self.overview_component=PersonroleOverviewComponent(None)
        
        row=self.overview_component.create_layout(self.layout_grid, row)
        
        row+=1
                    
    
    def add_uuid_row(self, label, row):
        uuid_label = Gtk.Label(label)
        uuid_label.set_justify(Gtk.Justification.LEFT)
        self.layout_grid.attach(uuid_label,0,row,1,1)
        self.uuid_text_entry=Gtk.Entry()
        self.uuid_text_entry.set_editable(False)
        self.layout_grid.attach(self.uuid_text_entry,1,row,1,1)
        

    def add_common_name_row(self, label, row):
        common_name_label = Gtk.Label(label)
        common_name_label.set_justify(Gtk.Justification.LEFT)
        self.layout_grid.attach(common_name_label,0,row,1,1)
        self.common_name_text_entry=Gtk.Entry()
        self.layout_grid.attach(self.common_name_text_entry,1,row,1,1)
        
    def add_current_object(self, widget):
        Personrole(sid=None,uuid=None,common_name=self.common_name_text_entry.get_text()).insert()
        self.overview_component.clean_and_populate_model()
        
    def parent_callback_func(self, widget, callback):
        print("in callback")


class PersonroleOverviewComponent(AbstractDataOverviewComponent):
    
    treecolumns=[TreeviewColumn("personrole_sid", 0, True),
                TreeviewColumn("Common name", 1, False)]
    
    def __init__(self, forecast):
        self.forecast=forecast
        super(PersonroleOverviewComponent, self).__init__(PersonroleOverviewComponent.treecolumns)
        
    
    def populate_model(self):
        self.treemodel.clear()
        for p in Personrole().get_all():
            self.treemodel.append(["%s" % p.sid, p.common_name])
                

