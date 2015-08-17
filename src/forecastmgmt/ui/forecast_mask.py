'''
Created on 14.03.2015

@author: vvladych
'''

from gi.repository import Gtk

from forecastmgmt.ui.forecast.forecast_overview_window import ForecastOverviewWindow

from forecastmgmt.ui.forecast.forecast_new_dialog import ForecastNewDialog

from ui_tools import add_column_to_treeview, show_info_dialog
from forecastmgmt.model.fc_project import FcProject
from abstract_mask import AbstractMask

class ForecastMask(AbstractMask):
    
    def __init__(self, main_window):
        super(ForecastMask, self).__init__(main_window)

        
        
    def create_overview_treeview(self):
        self.forecasts_treestore = Gtk.TreeStore(int,str,str,str)
        self.__populate_forecast_treestore()
        self.overview_treeview = Gtk.TreeView(self.forecasts_treestore)
        self.overview_treeview.append_column(add_column_to_treeview("id", 0, True))
        self.overview_treeview.append_column(add_column_to_treeview("Publisher", 1, False))
        self.overview_treeview.append_column(add_column_to_treeview("Date", 2, False))
        self.overview_treeview.append_column(add_column_to_treeview("Forecast", 3, False))
        
        
        
    def add_context_menu_overview_treeview(self):
        menu=Gtk.Menu()
        menu_item_create_new_forecast=Gtk.MenuItem("Add new forecast...")
        menu_item_create_new_forecast.connect("activate", self.on_menu_item_create_new_forecast_click) 
        menu.append(menu_item_create_new_forecast)
        menu_item_create_new_forecast.show()
        menu_item_delete_forecast=Gtk.MenuItem("Delete forecast...")
        menu_item_delete_forecast.connect("activate", self.on_menu_item_delete_forecast_click) 
        menu.append(menu_item_delete_forecast)
        menu_item_delete_forecast.show()
        self.overview_treeview.connect("button_press_event", self.on_treeview_button_press_event,menu)
        
        
        
    def on_menu_item_create_new_forecast_click(self,widget):
        new_forecast_dialog=ForecastNewDialog(None)
        response = new_forecast_dialog.run()
        
        if response==Gtk.ResponseType.OK:
            new_forecast_dialog.perform_insert()
                
        elif response==Gtk.ResponseType.CANCEL:
            show_info_dialog("Insert nothing")
        else:
            show_info_dialog("Unknown action")
        
        new_forecast_dialog.destroy()
        self.__populate_forecast_treestore()


    def __populate_forecast_treestore(self):
        self.forecasts_treestore.clear()
        for project in FcProject().get_all():
            self.forecasts_treestore.append(None,[project.sid,"","%s" % project.created_date,project.common_name])
            
             
    
    def on_menu_item_delete_forecast_click(self, widget):
        (model,tree_iter)=self.overview_treeview.get_selection().get_selected()    
        fc_project_sid=model.get_value(tree_iter,0)
        nd=Gtk.Dialog("Delete project", self.main_window, 0, ("OK", Gtk.ResponseType.OK, "CANCEL", Gtk.ResponseType.CANCEL))
        ret=nd.run()
        nd.destroy()
        if ret==Gtk.ResponseType.OK:
            FcProject(fc_project_sid).delete()
            self.__populate_forecast_treestore()
        else:
            show_info_dialog("Canceled")

        
    def on_treeview_button_press_event(self,treeview,event,widget):
        x = int(event.x)
        y = int(event.y)
        pthinfo=treeview.get_path_at_pos(x,y)
        if event.button==1:
            if pthinfo is not None:
                treeview.get_selection().select_path(pthinfo[0])    
                project_sid=self.forecasts_treestore.get(self.forecasts_treestore.get_iter(pthinfo[0]),0)
                self.project=FcProject(project_sid)
                self.project.load()
                self.clear_main_middle_pane()
                self.main_middle_pane.pack_start(ForecastOverviewWindow(self,self.project), False, False, 0)
                self.main_middle_pane.show_all()
        
        if event.button==3:
            if pthinfo is not None:
                treeview.get_selection().select_path(pthinfo[0])    
            widget.popup(None, None, None, None, event.button, event.time)    
        return True
