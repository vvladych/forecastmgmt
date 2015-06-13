'''
Created on 27.05.2015

@author: vvladych
'''
from gi.repository import Gtk

from forecastmgmt.ui.forecast.abstract_data_process_component import AbstractDataOverviewComponent, AbstractDataManipulationComponent, AbstractDataProcessComponent 

from forecastmgmt.ui.ui_tools import TreeviewColumn, show_info_dialog

from forecastmgmt.dao.db_connection import get_db_connection
import psycopg2.extras

from forecastmgmt.model.fc_object import FCObject
from forecastmgmt.model.fc_object_property import FCObjectProperty

class ModelProcessComponent(AbstractDataProcessComponent):
    
    def __init__(self, forecast):
        super(ModelProcessComponent, self).__init__(ModelManipulationComponent(forecast, ModelOverviewComponent(forecast)))
        

class ModelManipulationComponent(AbstractDataManipulationComponent):
    
    def __init__(self, forecast, overview_component):
        super(ModelManipulationComponent, self).__init__(overview_component)
        self.forecast=forecast
        
    def create_layout(self, parent_layout_grid, row):
        self.parent_layout_grid=parent_layout_grid
        row+=1
        # choose object property
        object_chooser_label = Gtk.Label("Choose object")
        object_chooser_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(object_chooser_label,0,row,1,1)
        
        self.object_combobox_model=self.populate_object_combobox_model()
        self.object_combobox=Gtk.ComboBox.new_with_model_and_entry(self.object_combobox_model)
        self.object_combobox.set_entry_text_column(1)
        self.object_combobox.connect("changed", self.on_object_combobox_changed)
        parent_layout_grid.attach(self.object_combobox,1,row,1,1)

        self.object_property_combobox_model=Gtk.ListStore(str,str)
        self.object_property_combobox_model.append(["1", "test"])
        self.object_property_combobox=Gtk.ComboBox.new_with_model_and_entry(self.object_property_combobox_model)
        self.object_property_combobox.set_entry_text_column(1)
        parent_layout_grid.attach(self.object_property_combobox,2,row,1,1)
        
        
        # set point-in-time
        row+=2
        
        pit_label=Gtk.Label("Choose point-in-time")
        pit_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(pit_label,0,row,1,1)
        
        self.state_date_day_textentry=Gtk.Entry()
        parent_layout_grid.attach(self.state_date_day_textentry,1,row,1,1)
        self.state_date_month_textentry=Gtk.Entry()
        parent_layout_grid.attach(self.state_date_month_textentry,2,row,1,1)
        self.state_date_year_textentry=Gtk.Entry()
        parent_layout_grid.attach(self.state_date_year_textentry,3,row,1,1)
        
        pit_choose_button=Gtk.Button("Pick date")
        parent_layout_grid.attach(pit_choose_button,4,row,1,1)
        pit_choose_button.connect("clicked", self.show_calendar)

        
        # set value
        row+=2
        object_property_value_label=Gtk.Label("Set value")
        object_property_value_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(object_property_value_label,0,row,1,1)
        
        self.object_property_value_textentry=Gtk.Entry()
        parent_layout_grid.attach(self.object_property_value_textentry,1,row,2,1)
        
        # TODO: set precondition(s)

        row+=2
        
        self.add_state_button=Gtk.Button("Add", Gtk.STOCK_ADD)
        parent_layout_grid.attach(self.add_state_button,0,row,1,1)
        self.add_state_button.connect("clicked", self.add_state_action)
                
        self.delete_button=Gtk.Button("Delete", Gtk.STOCK_DELETE)
        self.delete_button.connect("clicked", self.delete_action)        
        parent_layout_grid.attach(self.delete_button,1,row,1,1)

        
        # add / remove buttons
        
        # Add model text view
                
        row+=1

        return row
    
    def show_calendar(self, widget):
        self.calendar_window=Gtk.Dialog()
        self.calendar_window.action_area.hide()
        self.calendar_window.set_decorated(False)
        self.calendar_window.set_property('skip-taskbar-hint', True)
        self.calendar_window.set_size_request(200,200)
                
        self.calendar=Gtk.Calendar()
        self.calendar.connect('day-selected-double-click', self.day_selected, None)
        self.calendar_window.vbox.pack_start(self.calendar, True, True, 0)
        self.calendar.show()
        self.calendar_window.run()
        
        
    def day_selected(self, calendar, event):
        (year,month,day)=self.calendar.get_date()
        self.state_date_day_textentry.set_text("%s" % day)
        self.state_date_month_textentry.set_text("%s" % month)
        self.state_date_year_textentry.set_text("%s" % year)
        self.calendar_window.destroy()
    
    def get_active_object(self):
        tree_iter = self.object_combobox.get_active_iter()
        if tree_iter!=None:
            model = self.object_combobox.get_model()
            return model[tree_iter][0]
        else:
            print("please choose an object!")

    
    def on_object_combobox_changed(self, widget):
        self.populate_object_property_combobox_model(self.get_active_object())
        
    def populate_object_property_combobox_model(self, object_sid):
        self.object_property_combobox_model.clear()
        object_properties=FCObjectProperty().get_all_for_foreign_key(object_sid)
        for op in object_properties:
            self.object_property_combobox_model.append(["%s" % op.sid, op.common_name])
        
        
    def populate_object_combobox_model(self):
        combobox_model=Gtk.ListStore(str,str)
        object_list=FCObject().get_all()
        for o in object_list:
            combobox_model.append(["%s" % o.sid, o.common_name])
        return combobox_model
    
    def add_state_action(self, widget):
        print("add state")
        
    def delete_action(self, widget):
        print("delete chosen state")

    
class ModelOverviewComponent(AbstractDataOverviewComponent):
    
    treecolumns=[TreeviewColumn("model_text_sid", 0, True), TreeviewColumn("model text", 1, False)]

    
    def __init__(self, forecast):
        self.forecast=forecast
        super(ModelOverviewComponent, self).__init__(ModelOverviewComponent.treecolumns)
        
    def populate_model(self):
        print("hier")
        
