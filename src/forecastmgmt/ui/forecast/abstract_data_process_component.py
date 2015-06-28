'''
Created on 19.05.2015

@author: vvladych
'''

from gi.repository import Gtk

from forecastmgmt.ui.ui_tools import add_column_to_treeview


class AbstractDataProcessComponent(object):
    
    def __init__(self, data_manipulation_component):        
        self.data_manipulation_component=data_manipulation_component

        
    def create_layout(self, parent_layout_grid, row):
        return self.data_manipulation_component.create_layout(parent_layout_grid, row)
    
    
class AbstractDataManipulationComponent(object):
    
    def __init__(self, overview_component):
        self.overview_component=overview_component
    
    def create_layout(self, parent_layout_grid, row):
        raise NotImplementedError("create_layout still not implemented")
    
    

class AbstractDataOverviewComponent(object):
    
    def __init__(self, columns):
        if len(columns)>5:
            self.treemodel=Gtk.ListStore(str,str,str,str,str,str)
        else:
            self.treemodel=Gtk.ListStore(str,str,str,str,str)
        self.clean_and_populate_model()
        self.treeview=Gtk.TreeView(self.treemodel)
        for column in columns:
            self.treeview.append_column(add_column_to_treeview(column.column_name, column.ordernum, column.hidden))
        self.treeview.connect("row-activated", self.on_row_select)
        self.treeview.set_size_request(200,100)
        
            
    def create_layout(self, parent_layout_grid, row):
        raise NotImplementedError("create_layout still not implemented!")
            
        
    def clean_and_populate_model(self):
        self.treemodel.clear()
        self.populate_model()
        
        
    def populate_model(self):
        raise NotImplementedError("populate_model still not implemented!")
    
    def on_row_select(self,widget,path,data):
        raise NotImplementedError("on_row_select still not implemented!")