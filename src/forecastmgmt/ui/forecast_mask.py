'''
Created on 14.03.2015

@author: vvladych
'''

from gi.repository import Gtk

from forecastmgmt.ui.forecast.forecast_overview_window import ForecastOverviewWindow


from ui_tools import add_column_to_treeview
from forecastmgmt.model.fc_project import FcProject, get_project_list

class ForecastMask(Gtk.Grid):
    
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
        self.forecasts_treeview.connect("row-activated", self.on_row_select)
        self.forecasts_treeview.set_size_request(200,300)
        
        
        
    def __populate_forecast_treestore(self):
        for project in get_project_list():
            self.forecasts_treestore.append(None,[project.sid,project.common_name])
            
    def __clear_main_middle_pane(self):
        for child in self.main_middle_pane.get_children():
            self.main_middle_pane.remove(child)        
             
        
    def on_row_select(self,widget,path,data):
        project_sid=self.forecasts_treestore.get(self.forecasts_treestore.get_iter(path),0)
        project=FcProject(project_sid)
        project.load()
        self.__clear_main_middle_pane()
        self.main_middle_pane.pack_start(ForecastOverviewWindow(self,project), False, False, 0)
        self.main_middle_pane.show_all()
        
