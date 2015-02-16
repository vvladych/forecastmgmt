
from gi.repository import Gtk
from forecastmgmt.dao.person_dao import PersonDAO
from forecastmgmt.dao.person_name_dao import get_person_name_roles
from forecastmgmt.dao.namepart_dao import get_name_part_roles

class PersonAddMask(Gtk.Grid):
    def __init__(self, reset_callback, main_window):
        Gtk.Grid.__init__(self)

        self.main_window=main_window

        self.set_column_spacing(5)

        placeholder_label = Gtk.Label("")
        placeholder_label.set_size_request(1,40)
        self.attach(placeholder_label,0,-1,1,1)
        # Row 0: person uuid
        uuid_label = Gtk.Label("person UUID")
        self.attach(uuid_label,0,0,1,1)
        uuid_text_entry=Gtk.Entry()
        self.attach(uuid_text_entry,1,0,1,1)

        # Row 1: name 
        name_label = Gtk.Label("Name")
        self.attach(name_label,0,1,1,1)

        self.name_roles_model=self.populate_name_roles_model()
        self.name_role_combobox=Gtk.ComboBox.new_with_model_and_entry(self.name_roles_model)
        self.name_role_combobox.set_entry_text_column(1)
        self.name_role_combobox.set_active(0)
        self.attach(self.name_role_combobox,1,1,1,1)

        name_add_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        name_add_button.connect("clicked", self.add_name)
        self.attach(name_add_button,2,1,1,1)

        name_delete_button = Gtk.Button("Delete", Gtk.STOCK_DELETE)
        name_delete_button.connect("clicked", self.delete_name)
        self.attach(name_delete_button,3,1,1,1)
        
        # Row 2: name part role
        namepart_label = Gtk.Label("Name part")
        self.attach(namepart_label,0,2,1,1)

        namepart_add_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        namepart_add_button.connect("clicked", self.add_name_part) 
        self.attach(namepart_add_button,2,2,1,1)

        namepart_add_button = Gtk.Button("Delete", Gtk.STOCK_DELETE)
        namepart_add_button.connect("clicked", self.delete_name_part) 
        self.attach(namepart_add_button,3,2,1,1)

        self.namepart_roles_model = self.populate_namepart_roles_model()
        self.namepart_role_combobox=Gtk.ComboBox.new_with_model_and_entry(self.namepart_roles_model)
        self.namepart_role_combobox.set_entry_text_column(1)
        self.namepart_role_combobox.set_active(0)

        self.attach(self.namepart_role_combobox,1,2,1,1)

        # Row 3: name part value
        self.namepart_role_value_entry = Gtk.Entry()
        self.attach(self.namepart_role_value_entry,1,3,1,1)

        # Row 4: treeview 
        self.create_namepart_treeview()
        self.attach(self.nameparts_treeview,0,4,3,1)

        # Row 5
        save_button = Gtk.Button("save", Gtk.STOCK_SAVE)
        save_button.connect("clicked", self.save_person)
        self.attach(save_button,1,5,1,1)

        new_button = Gtk.Button("New", Gtk.STOCK_NEW)
        new_button.connect("clicked", self.new_person_func)
        self.attach(new_button,2,5,1,1)

        cancel_button = Gtk.Button("Cancel", Gtk.STOCK_CANCEL)
        cancel_button.connect("clicked", self.parent_callback_func, reset_callback)
        self.attach(cancel_button,3,5,1,1)

    def add_name(self,widget):
        name_role_id,name_role_value = self.get_active_name_role()
        self.namepart_treestore.append(None,[name_role_id,name_role_value,None])

    def delete_name(self,widget):
        print("delete_name: unimplemented")

    def get_active_name_role(self):
        name_combobox_iter = self.name_role_combobox.get_active_iter()
        if name_combobox_iter!=None:
            model = self.name_roles_model
            name = model[name_combobox_iter][:2]
        else:
            row_id=0
            name=self.name_role_combobox.get_child()
        return name

    def new_person_func(self, widget):
        print("new person: unimplemented")

    def save_person(self, widget):
        print("save person: unimplemented")

    def get_active_name_treestore(self):
        model,tree_iter=self.nameparts_treeview.get_selection().get_selected()
        return tree_iter

    # NamePart
    def delete_name_part(self, callback):
        model,tree_iter = self.nameparts_treeview.get_selection().get_selected()
        model.remove(tree_iter)

    def add_name_part(self,callback):
        namepart_role_id,namepart_role_value=self.get_active_namepart_role()
        tree_iter=self.get_active_name_treestore()

        if tree_iter==None:
            message = Gtk.MessageDialog(self.main_window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error: name part cannot be added as root element")
            message.run()
            return

        if self.namepart_treestore.iter_depth(tree_iter)!=0:
            message = Gtk.MessageDialog(self.main_window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Error: name part can be added to a root element only")
            message.run()
            return

        self.namepart_treestore.append(tree_iter,[namepart_role_id,namepart_role_value,self.namepart_role_value_entry.get_text()])
        self.namepart_role_value_entry.set_text('')
            
    def get_active_namepart_role(self):
        tree_iter = self.namepart_role_combobox.get_active_iter()
        if tree_iter!=None:
            model = self.namepart_role_combobox.get_model()
            name = model[tree_iter][:2]
        else:
            row_id=0
            name = self.namepart_role_combobox.get_child()
        return name


    def create_namepart_treeview(self):
        self.namepart_treestore = Gtk.TreeStore(int,str,str)
        self.nameparts_treeview = Gtk.TreeView(self.namepart_treestore)
        self.nameparts_treeview.append_column(self.add_column_to_treeview("id", 0, True))
        self.nameparts_treeview.append_column(self.add_column_to_treeview("Role", 1, False))
        self.nameparts_treeview.append_column(self.add_column_to_treeview("Value", 2, False))
        self.nameparts_treeview.set_size_request(200,300)
        self.nameparts_treeview.connect("row-activated", self.on_row_selection)

    def on_row_selection(self,treeview,path,column):
        model,treeiter=self.nameparts_treeview.get_selection().get_selected()
        self.namepart_role_combobox.set_active(model[treeiter][0])
        self.namepart_role_value_entry.set_text(model[treeiter][2])
        

    def add_column_to_treeview(self,columnname,counter,hidden):
        column=Gtk.TreeViewColumn(columnname)
        if hidden==True:
            column.set_visible(False)
        renderer=Gtk.CellRendererText()
        column.pack_start(renderer,True)
        column.add_attribute(renderer, "text", counter)
        return column

    def populate_namepart_roles_model(self):
        namepart_roles_model = Gtk.ListStore(int, str)
        namepart_roles_list=get_name_part_roles()
        counter=0
        for namepart_role in namepart_roles_list:
            namepart_roles_model.append([counter,namepart_role])
            counter+=1
        return namepart_roles_model

    def populate_name_roles_model(self):
        name_roles_model = Gtk.ListStore(int,str)
        nameroles_list = get_person_name_roles()
        counter=0
        for namerole in nameroles_list:
            name_roles_model.append([counter,namerole])
            counter+=1
        return name_roles_model

    def parent_callback_func(self, widget, cb_func=None):
        print("in reset_callback")
        cb_func()
