'''
Created on 27.05.2015

@author: vvladych
'''
from gi.repository import Gtk

from forecastmgmt.ui.forecast.abstract_data_process_component import AbstractDataOverviewComponent, AbstractDataManipulationComponent, AbstractDataProcessComponent 

from forecastmgmt.ui.ui_tools import TreeviewColumn, show_info_dialog

from forecastmgmt.dao.db_connection import get_db_connection
import psycopg2.extras

import datetime


from forecastmgmt.model.fc_object import FCObject
from forecastmgmt.model.fc_object_property import FCObjectProperty
from forecastmgmt.model.fc_object_property_state import FCObjectPropertyState

class ModelStateProcessComponent(AbstractDataProcessComponent):
    
    def __init__(self, forecast):
        super(ModelStateProcessComponent, self).__init__(ModelStateManipulationComponent(forecast, ModelStateOverviewComponent(forecast)))
        

class ModelStateManipulationComponent(AbstractDataManipulationComponent):
    
    def __init__(self, fcmodel, overview_component):
        super(ModelStateManipulationComponent, self).__init__(overview_component)
        self.fcmodel=fcmodel
        
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
        
        row+=2
        
        self.add_state_button=Gtk.Button("Add", Gtk.STOCK_ADD)
        parent_layout_grid.attach(self.add_state_button,0,row,1,1)
        self.add_state_button.connect("clicked", self.add_state_action)
                
        self.delete_button=Gtk.Button("Delete", Gtk.STOCK_DELETE)
        self.delete_button.connect("clicked", self.delete_action)        
        parent_layout_grid.attach(self.delete_button,1,row,1,1)

        row+=3
        
        row=self.overview_component.create_layout(parent_layout_grid, row)
        
        row += 1

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
            

    def get_active_object_property(self):
        tree_iter = self.object_property_combobox.get_active_iter()
        if tree_iter!=None:
            model = self.object_property_combobox.get_model()
            object_property_sid = model[tree_iter][:2]
            return object_property_sid
        else:
            print("please choose a person!")
        
    
    
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
    
    
    def get_point_in_time(self):
        return datetime.date(int(self.state_date_year_textentry.get_text()), 
                                    int(self.state_date_month_textentry.get_text()), 
                                    int(self.state_date_day_textentry.get_text()))
        
    def get_object_property_state_value(self):
        return self.object_property_value_textentry.get_text()
    
    def add_state_action(self, widget):
        # get object property
        (object_property_sid,object_property_common_name)=self.get_active_object_property()
        # insert new state
        FCObjectPropertyState(None,object_property_sid,self.get_point_in_time(),self.get_object_property_state_value()).insert()
        # 
        show_info_dialog("Add successful")
        self.overview_component.clean_and_populate_model()
        
        
    def delete_action(self, widget):
        print("delete chosen state")

    
class ModelStateOverviewComponent(AbstractDataOverviewComponent):
    
    treecolumns=[TreeviewColumn("state_sid", 0, False), TreeviewColumn("object_property_sid", 1, True), 
                TreeviewColumn("fc_project_sid", 2, True), TreeviewColumn("Object property", 3, False),
                TreeviewColumn("State PIT", 4, False), TreeviewColumn("Property Value", 5, False)]

    
    def __init__(self, fcmodel):
        self.fcmodel=fcmodel
        super(ModelStateOverviewComponent, self).__init__(ModelStateOverviewComponent.treecolumns)
        

    def create_layout(self, parent_layout_grid, row):
        row += 1
        
        parent_layout_grid.attach(self.treeview,0,row,4,1)
                
        return row

        
    def populate_model(self):
        self.treemodel.clear()
        cur=get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        #data=(self.fcmodel.sid,)
        #cur.execute("""SELECT 
        #                1,1,1,'test','12.02.2012','value'
        #                """,data)

#        for p in cur.fetchall():
#            self.treemodel.append([])
        self.treemodel.append(['1','1','1','test','12.02.2012','value'])
        cur.close()

        
