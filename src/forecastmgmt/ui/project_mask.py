'''
Created on 14.03.2015

@author: vvladych
'''

from gi.repository import Gtk

from project_overview_window import ProjectOverviewWindow


from ui_tools import add_column_to_treeview
from forecastmgmt.model.fc_project import FcProject, get_project_list

class ProjectMask(Gtk.Grid):
    
    def __init__(self, main_window, person=None):
        Gtk.Grid.__init__(self)

        self.main_window=main_window

        # Main working pane: contains left pane with actions and working area pane 
        self.main_working_pane=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(self.main_working_pane)

        # the left pane: actions
        self.main_left_pane = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        # the middle pane: working area
        self.main_middle_pane = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
                       
        self.main_working_pane.pack_start(self.main_left_pane, False, False, 0)
        self.main_working_pane.pack_start(self.main_middle_pane, False, False, 0)
        
        self.create_main_left_pane()
        
        
    def create_main_left_pane(self):
        self.__create_forecast_list_treeview()
        self.main_left_pane.pack_start(self.forecasts_treeview, False, False, 0)   
        
        
    def __create_forecast_list_treeview(self):
        self.forecasts_treestore = Gtk.TreeStore(int,str)
        self.__populate_forecast_treestore()
        self.forecasts_treeview = Gtk.TreeView(self.forecasts_treestore)
        self.forecasts_treeview.append_column(add_column_to_treeview("id", 0, True))
        self.forecasts_treeview.append_column(add_column_to_treeview("Forecast", 1, False))
        
        self.forecasts_treeview.set_size_request(200,300)
        
        
        
    def __populate_forecast_treestore(self):
        for project in get_project_list():
            self.forecasts_treestore.append(None,[project.sid,project.common_name])
             
        
        
    def set_main_area(self, main_area_type="forecast"):
        if main_area_type=="forecast":
            self.main_middle_pane.pack_start(ProjectOverviewWindow(self), False, False, 0)
        #elif main_area_type=="organization":
        #    self.main_middle_pane.pack_start(OrganisationMask(), False, False, 0)
        else:
            print("unimplemented")
