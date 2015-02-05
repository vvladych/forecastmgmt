
from gi.repository import Gtk
from forecastmgmt.dao.person_dao import PersonDAO

class PersonAddMask(Gtk.Grid):
    def __init__(self, reset_callback):
        Gtk.Grid.__init__(self)
        self.set_column_spacing(5)

        placeholder_label = Gtk.Label("")
        placeholder_label.set_size_request(1,40)
        self.attach(placeholder_label,0,-1,1,1)

        uuid_label = Gtk.Label("person UUID")
        self.attach(uuid_label,0,0,1,1)
        uuid_text_entry=Gtk.Entry()
        self.attach(uuid_text_entry,1,0,1,1)

        namepart_label = Gtk.Label("Name part")
        self.attach(namepart_label,0,1,1,1)

        namepart_add_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        namepart_add_button.connect("clicked", self.process_name_part) 
        self.attach(namepart_add_button,2,1,1,1)

        self.namepart_roles_model = self.populate_namepart_roles_model()
        self.namepart_role_combobox=Gtk.ComboBox.new_with_model_and_entry(self.namepart_roles_model)
        self.namepart_role_combobox.set_entry_text_column(1)
        self.namepart_role_combobox.set_active(0)

        self.attach(self.namepart_role_combobox,1,1,1,1)

        self.namepart_role_value_entry = Gtk.Entry()
        self.attach(self.namepart_role_value_entry,1,2,1,1)

        self.create_namepart_treeview()
        self.attach(self.nameparts_treeview,0,3,3,1)

        test_button = Gtk.Button("Test", Gtk.STOCK_OK)
        test_button.connect("clicked", self.parent_callback_func, reset_callback)
        self.attach(test_button,1,4,1,1)

    def process_name_part(self,callback):
        namepart_role_id,namepart_role_value=self.get_active_namepart_role()
        self.namepart_liststore.append([namepart_role_id,namepart_role_value,self.namepart_role_value_entry.get_text()])
        self.namepart_role_value_entry.set_text('')

    def get_active_namepart_role(self):
        tree_iter = self.namepart_role_combobox.get_active_iter()
        if tree_iter!=None:
            model = self.namepart_role_combobox.get_model()
            name = model[tree_iter][:2]
            print("hier guck %s" % model[tree_iter][:1])
            print(name)
        else:
            print("hier 20")
            row_id=0
            name = self.namepart_role_combobox.get_child()
        return name


    def create_namepart_treeview(self):
        self.namepart_liststore = Gtk.ListStore(int,str,str)
        self.nameparts_treeview = Gtk.TreeView(self.namepart_liststore)
        self.nameparts_treeview.append_column(self.add_column_to_treeview("roleid", 0, True))
        self.nameparts_treeview.append_column(self.add_column_to_treeview("Role", 1, False))
        self.nameparts_treeview.append_column(self.add_column_to_treeview("Value", 2, False))
        self.nameparts_treeview.set_size_request(200,300)
        self.nameparts_treeview.connect("row-activated", self.on_row_selection)

    def on_row_selection(self,treeview,path,column):
        model,treeiter=self.nameparts_treeview.get_selection().get_selected()
        self.namepart_role_combobox.set_active(model[treeiter][0])
        print("hier??? %s" % model[treeiter][0]) 
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
        namepart_roles_model.append([0,"Surname"])
        namepart_roles_model.append([1,"Given name"])
        return namepart_roles_model

    def parent_callback_func(self, widget, cb_func=None):
        print("in reset_callback")
        cb_func()
