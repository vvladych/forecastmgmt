from gi.repository import Gtk


from forecastmgmt.ui.masterdata_mask import MasterdataMask
from forecastmgmt.ui.forecast_mask import ForecastMask

from forecastmgmt.ui.forecast.forecast_new_dialog import ForecastNewDialog


class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Forecaster")
        self.set_default_size(800,600)
        
        # The main area, grid 
        self.grid = Gtk.Grid()
        self.grid.set_orientation(Gtk.Orientation.VERTICAL)
        self.add(self.grid)

        menubar=self.create_menubar()
        self.grid.add(menubar)
        
        toolbar=self.create_toolbar()       
        self.grid.add(toolbar)
        
        self.working_area=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.grid.add(self.working_area)
        self.set_working_area("forecast")

        self.create_status_bar()
        #self.grid.add(self.statusbar)
        
    
    def create_status_bar(self):
        self.statusbar = Gtk.Statusbar()
        self.statusbar.add(Gtk.Label("statusbar"))

        
    def create_toolbar(self):
        toolbar=Gtk.Toolbar()

        toolbutton_forecast=Gtk.ToolButton(Gtk.STOCK_ABOUT)
        toolbutton_forecast.set_tooltip_text("forecast")
        toolbutton_forecast.connect("clicked", self.on_toolbutton_forecast)
        toolbar.add(toolbutton_forecast)


        toolbutton_master_data=Gtk.ToolButton(Gtk.STOCK_EXECUTE)
        toolbutton_master_data.set_tooltip_text("master data")
        toolbutton_master_data.connect("clicked", self.on_toolbutton_masterdata)
        toolbar.add(toolbutton_master_data)
        
        
        toolbutton_quit=Gtk.ToolButton(Gtk.STOCK_QUIT)
        toolbutton_quit.set_tooltip_text("quit")
        toolbutton_quit.connect("clicked", self.on_menu_file_quit)
        toolbar.add(toolbutton_quit)

        return toolbar 
    
    
    def create_menubar(self):
        menubar = Gtk.MenuBar()
        
        file_menu_entry = Gtk.MenuItem("File")
        
        menu = Gtk.Menu()
        mitem_file_new=Gtk.MenuItem("New forecast...")
        
        mitem_quit = Gtk.MenuItem("Quit")
        mitem_quit.connect("activate", self.on_menu_file_quit)
        menu.insert(mitem_file_new, 0)
        menu.insert(mitem_quit, 1)
        
        file_menu_entry.set_submenu(menu)
        
        
        menubar.append(file_menu_entry)
        
        return menubar
       
    
    def clean_working_area(self):
        for child in self.working_area.get_children():
            self.working_area.remove(child)
            
    def set_working_area(self, action="masterdata"):
        self.clean_working_area()
        if action=="masterdata":
            self.working_area.pack_start(MasterdataMask(self), False, False, 0)
        elif action=="forecast":
            self.working_area.pack_start(ForecastMask(self), False, False, 0)
        else:
            print("unimplemented")

        self.working_area.show_all()
        
        
    def on_menu_file_quit(self, widget):
        Gtk.main_quit()
        

    def on_toolbutton_masterdata(self, widget):
        self.set_working_area("masterdata")
        
        
    def on_toolbutton_forecast(self, widget):
        self.set_working_area("forecast")
        
    def on_new_forecast(self, widget):
        new_forecast_dialog=ForecastNewDialog(self)
        response = new_forecast_dialog.run()
        
        if response==Gtk.ResponseType.OK:
            new_forecast_dialog.perform_insert()
            self.clean_working_area()
            self.set_working_area("forecast")
                
        elif response==Gtk.ResponseType.CANCEL:
            print("insert nothing")
        else:
            print("unknown action")
        
        new_forecast_dialog.destroy()

            

win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
