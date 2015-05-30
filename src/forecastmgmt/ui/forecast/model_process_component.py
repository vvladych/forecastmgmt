'''
Created on 27.05.2015

@author: vvladych
'''
from gi.repository import Gtk

from forecastmgmt.ui.forecast.abstract_data_process_component import AbstractDataOverviewComponent, AbstractDataManipulationComponent, AbstractDataProcessComponent 

from forecastmgmt.ui.ui_tools import TreeviewColumn, show_info_dialog

from forecastmgmt.dao.db_connection import get_db_connection
import psycopg2.extras

class ModelProcessComponent(AbstractDataProcessComponent):
    
    def __init__(self, forecast):
        super(ModelProcessComponent, self).__init__(ModelManipulationComponent(forecast, ModelOverviewComponent(forecast)))
        

class ModelManipulationComponent(AbstractDataManipulationComponent):
    
    def __init__(self, forecast, overview_component):
        super(ModelManipulationComponent, self).__init__(overview_component)
        self.forecast=forecast
        
    def create_layout(self, parent_layout_grid, row):
        row+=1
        # Add model text view
        scrolledwindow= Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.forecast_model_textview=Gtk.TextView()
        scrolledwindow.add(self.forecast_model_textview)
        parent_layout_grid.attach(scrolledwindow,0,row,1,1)
                
        row+=1
        # Add save button
        self.save_model_button=Gtk.Button("Save", Gtk.STOCK_SAVE)
        parent_layout_grid.attach(self.save_model_button,1,row,1,1)
        self.save_model_button.connect("clicked", self.save_model_action)
        
    def save_model_action(self, widget):
        pass

    
class ModelOverviewComponent(AbstractDataOverviewComponent):
    
    treecolumns=[TreeviewColumn("publication_sid", 0, True)]

    
    def __init__(self, forecast):
        self.forecast=forecast
        super(ModelOverviewComponent, self).__init__(ModelOverviewComponent.treecolumns)
        

    def populate_model(self):
        pass