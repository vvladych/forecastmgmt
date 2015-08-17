'''
Created on 14.03.2015

@author: vvladych
'''

from gi.repository import Gtk

from forecastmgmt.ui.forecast.forecast_overview_window import ForecastOverviewWindow

from forecastmgmt.ui.forecast.forecast_new_dialog import ForecastNewDialog

from ui_tools import add_column_to_treeview, show_info_dialog
from forecastmgmt.model.fc_project import FcProject

class ForecastMask(Gtk.Grid):
    
    def __init__(self, main_window, person=None):
        Gtk.Grid.__init__(self)

        self.main_window=main_window
        self.project=None

        # Main working pane: contains left pane with actions and working area pane 
        self.main_working_pane=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_working_pane.set_size_request(200,600)
        self.add(self.main_working_pane)

        # the left pane: actions
        self.main_left_pane = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # the middle pane: working area
        self.main_middle_pane = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
                       
        self.main_working_pane.pack_start(self.main_left_pane, False, False, 0)
        self.main_working_pane.pack_start(self.main_middle_pane, False, False, 0)
        
        self.create_main_left_pane()
        
        
    def create_main_left_pane(self):
        self.__create_forecast_list_treeview()
        self.main_left_pane.pack_start(self.forecasts_treeview, False, False, 0)  
        
        
    def __create_forecast_list_treeview(self):
        self.forecasts_treestore = Gtk.TreeStore(int,str,str,str)
        self.__populate_forecast_treestore()
        self.forecasts_treeview = Gtk.TreeView(self.forecasts_treestore)
        self.forecasts_treeview.append_column(add_column_to_treeview("id", 0, True))
        self.forecasts_treeview.append_column(add_column_to_treeview("Publisher", 1, False))
        self.forecasts_treeview.append_column(add_column_to_treeview("Date", 2, False))
        self.forecasts_treeview.append_column(add_column_to_treeview("Forecast", 3, False))
        self.__add_context_menu_forecast_treeview()
        self.forecasts_treeview.set_size_request(200,300)
        
    def __add_context_menu_forecast_treeview(self):
        menu=Gtk.Menu()
        menu_item_create_new_forecast=Gtk.MenuItem("Add new forecast...")
        menu_item_create_new_forecast.connect("activate", self.on_menu_item_create_new_forecast_click) 
        menu.append(menu_item_create_new_forecast)
        menu_item_create_new_forecast.show()
        menu_item_delete_forecast=Gtk.MenuItem("Delete forecast...")
        menu_item_delete_forecast.connect("activate", self.on_menu_item_delete_forecast_click) 
        menu.append(menu_item_delete_forecast)
        menu_item_delete_forecast.show()
        self.forecasts_treeview.connect("button_press_event", self.on_treeview_button_press_event,menu)
        
        
        
    def on_menu_item_create_new_forecast_click(self,widget):
        new_forecast_dialog=ForecastNewDialog(None)
        response = new_forecast_dialog.run()
        
        if response==Gtk.ResponseType.OK:
            new_forecast_dialog.perform_insert()
                
        elif response==Gtk.ResponseType.CANCEL:
            print("insert nothing")
        else:
            print("unknown action")
        
        new_forecast_dialog.destroy()
        self.__populate_forecast_treestore()


    def __populate_forecast_treestore(self):
        self.forecasts_treestore.clear()
        for project in FcProject().get_all():
            self.forecasts_treestore.append(None,[project.sid,"","%s" % project.created_date,project.common_name])
            
    def __clear_main_middle_pane(self):
        for child in self.main_middle_pane.get_children():
            self.main_middle_pane.remove(child)        
             
    
    def on_menu_item_delete_forecast_click(self, widget):
        print("delete...")
        (model,tree_iter)=self.forecasts_treeview.get_selection().get_selected()    
        print("delete forecast_sid: %s" % model.get_value(tree_iter,0))
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
                self.__clear_main_middle_pane()
                self.main_middle_pane.pack_start(ForecastOverviewWindow(self,self.project), False, False, 0)
                self.main_middle_pane.show_all()
        
        if event.button==3:
            if pthinfo is not None:
                treeview.get_selection().select_path(pthinfo[0])    
            widget.popup(None, None, None, None, event.button, event.time)    
        return True
