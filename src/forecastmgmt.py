from gi.repository import Gtk

from forecastmgmt.ui.person_list_mask import PersonListMask 


class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Forecaster")
        self.set_default_size(800,600)
        
        action_group=Gtk.ActionGroup("my_actions")
        
        self.add_file_menu_actions(action_group)
        
        uimanager=self.create_ui_manager()
        uimanager.insert_action_group(action_group)        

        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        toolbar = uimanager.get_widget("/ToolBar")
        menubar = uimanager.get_widget("/MenuBar")

        main_vbox.pack_start(menubar, False, False, 0)
        main_vbox.pack_start(toolbar, False, False, 0)               
        self.set_main_area()
        main_vbox.pack_start(self.create_main_area(), True, True, 0)
        self.create_status_bar()
        main_vbox.pack_start(self.statusbar, False, False, 0)
        self.add(main_vbox)
        
    # 
    # set main working area
    # 
    def create_main_area(self):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox.pack_start(self.mask_chooser(), False, False, 0)

        mask = self.main_area
        hbox.pack_start(mask.get_view(), True, True, 0)
        return hbox
    
    
    def set_main_area(self, main_area_type="person"):
        if main_area_type=="person":
            self.main_area=PersonListMask()
        elif main_area_type=="organization":
            self.main_area=OrganisationMask()
        else:
            print("unimplemented")
    
    def mask_chooser(self):
        vbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # add empty Label
        vbox.pack_start(Gtk.Label(" "), False, False, 0)
        
        # add mask chooser
        mask_store = Gtk.ListStore(int, str)
        mask_store.append([1, "Person"])
        mask_store.append([2, "Organisation"])
        mask_combo = Gtk.ComboBox.new_with_model_and_entry(mask_store)
        mask_combo.set_entry_text_column(1)
        mask_combo.connect("changed", self.mask_combo_changed)
        mask_combo.set_active(0)
        vbox.pack_start(mask_combo, False, False, 0)
        return vbox
    
    def mask_combo_changed(self, mask_combo):
        if mask_combo.get_active()==0:
            self.set_main_area("person")
        elif mask_combo.get_active()==1:
            self.set_main_area("organisation")
        else:
            print("unimplemented")
    
    def create_status_bar(self):
        self.statusbar = Gtk.Statusbar()
        self.statusbar.add(Gtk.Label("statusbar"))

        
    def create_ui_manager(self):
        UI_INFO="""
            <ui>
                <menubar name='MenuBar'>
                    <menu action='FileMenu'>
                    
                        <menu action='FileNew'>
                            <menuitem action='FileNewStandard'/>
                            <menuitem action='FileNewFoo'/>
                        </menu>     <!-- FileNew -->                                            
                    
                    <separator/>
                    
                    <menuitem action='FileQuit'/>
                    
                    </menu>      <!-- FileMenu -->
                    
                </menubar>    <!-- MenuBar -->
                <toolbar name='ToolBar'>
                    <toolitem action='FileNewStandard' />
                    <toolitem action='FileQuit' />
                </toolbar>                
                
            </ui>
        """

        uimanager = Gtk.UIManager()
        uimanager.add_ui_from_string(UI_INFO)
        
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        return uimanager
        

        
    def add_file_menu_actions(self, action_group):
        action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        action_group.add_action(action_filemenu)
        
        action_filenewmenu = Gtk.Action("FileNew", None, None, Gtk.STOCK_NEW)
        action_group.add_action(action_filenewmenu)
        
        action_new = Gtk.Action("FileNewStandard", "_New", "Create a new file", Gtk.STOCK_NEW)
        action_new.connect("activate", self.on_menu_file_new_generic)
        action_group.add_action_with_accel(action_new, None)
        
        action_group.add_actions([
            ("FileNewFoo", None, "New Foo", None, "Create new foo", self.on_menu_file_new_generic),
        ])
        
        action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
        action_filequit.connect("activate", self.on_menu_file_quit)
        action_group.add_action(action_filequit)


    def on_menu_file_new_generic(self, widget):
        print("A File|New menu item was selected")
        
    def on_menu_file_quit(self, widget):
        Gtk.main_quit()
            
    def on_button_clicked(self, widget):
        print("Hello World")

win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
