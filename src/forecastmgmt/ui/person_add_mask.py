
from gi.repository import Gtk
from forecastmgmt.dao.person_dao import PersonDAO
from forecastmgmt.dao.namepart_dao import NamepartDAO
from forecastmgmt.dao.person_name_dao import PersonNameDAO

from forecastmgmt.model.person import Person
from forecastmgmt.model.namepart import Namepart
from forecastmgmt.model.person_name import PersonName


from forecastmgmt.dao.person_name_dao import get_person_name_roles
from forecastmgmt.dao.namepart_dao import get_name_part_roles

from forecastmgmt.dao.db_connection import get_db_connection


class PersonAddMask(Gtk.Grid):
    def __init__(self, reset_callback, main_window, person=None):
        Gtk.Grid.__init__(self)

        self.main_window=main_window
        self.reset_callback = reset_callback
        
        self.create_layout()
        
        if person!=None:
            self.load_person(person)

        
        
    def create_layout(self):
        self.set_column_spacing(5)

        placeholder_label = Gtk.Label("")
        placeholder_label.set_size_request(1,40)
        self.attach(placeholder_label,0,-1,1,1)

        row = 0
        # Row 0: person uuid
        uuid_label = Gtk.Label("person UUID")
        self.attach(uuid_label,0,row,1,1)
        uuid_text_entry=Gtk.Entry()
        self.attach(uuid_text_entry,1,row,1,1)
        
        row+=1
        # Row 1: common name
        common_name_label = Gtk.Label("Common Name")
        self.attach(common_name_label,0,row,1,1)
        self.common_name_text_entry=Gtk.Entry()
        self.attach(self.common_name_text_entry,1,row,1,1)

        row+=1
        # Row: birth date
        birth_date_label = Gtk.Label("Birth Date")
        self.attach(birth_date_label,0,row,1,1)
        self.birth_date_text_entry=Gtk.Entry()
        self.attach(self.birth_date_text_entry,1,row,1,1)

        row+=1
        
        # Row: birth place
        birth_place_label = Gtk.Label("Birth Place")
        self.attach(birth_place_label,0,row,1,1)
        self.birth_place_text_entry=Gtk.Entry()
        self.attach(self.birth_place_text_entry,1,row,1,1)

        row+=1
        
        # Row 2: name 
        name_label = Gtk.Label("Name")
        self.attach(name_label,0,row,1,1)

        self.name_roles_model=self.populate_name_roles_model()
        self.name_role_combobox=Gtk.ComboBox.new_with_model_and_entry(self.name_roles_model)
        self.name_role_combobox.set_entry_text_column(1)
        self.name_role_combobox.set_active(0)
        self.attach(self.name_role_combobox,1,row,1,1)

        name_add_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        name_add_button.connect("clicked", self.add_name)
        self.attach(name_add_button,2,row,1,1)

        name_delete_button = Gtk.Button("Delete", Gtk.STOCK_DELETE)
        name_delete_button.connect("clicked", self.delete_name)
        self.attach(name_delete_button,3,row,1,1)
        
        row+=1
        # Row 2: name part role
        namepart_label = Gtk.Label("Name part")
        self.attach(namepart_label,0,row,1,1)

        namepart_add_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        namepart_add_button.connect("clicked", self.add_name_part) 
        self.attach(namepart_add_button,2,row,1,1)

        namepart_add_button = Gtk.Button("Delete", Gtk.STOCK_DELETE)
        namepart_add_button.connect("clicked", self.delete_name_part) 
        self.attach(namepart_add_button,3,row,1,1)

        self.namepart_roles_model = self.populate_namepart_roles_model()
        self.namepart_role_combobox=Gtk.ComboBox.new_with_model_and_entry(self.namepart_roles_model)
        self.namepart_role_combobox.set_entry_text_column(1)
        self.namepart_role_combobox.set_active(0)

        self.attach(self.namepart_role_combobox,1,row,1,1)

        row+=1
        # Row 3: name part value
        self.namepart_role_value_entry = Gtk.Entry()
        self.attach(self.namepart_role_value_entry,1,row,1,1)

        row+=1
        # Row 4: treeview 
        self.create_namepart_treeview()
        self.attach(self.nameparts_treeview,0,row,3,1)

        row+=1
        # Row 5
        save_button = Gtk.Button("save", Gtk.STOCK_SAVE)
        save_button.connect("clicked", self.save_person)
        self.attach(save_button,1,row,1,1)

        new_button = Gtk.Button("New", Gtk.STOCK_NEW)
        new_button.connect("clicked", self.new_person_func)
        self.attach(new_button,2,row,1,1)

        cancel_button = Gtk.Button("Cancel", Gtk.STOCK_CANCEL)
        cancel_button.connect("clicked", self.parent_callback_func, self.reset_callback)
        self.attach(cancel_button,3,row,1,1)
        
        
    def load_person(self, person_to_load):
        print("still unimplemented")
        

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
            name=self.name_role_combobox.get_child()
        return name

    def new_person_func(self, widget):
        print("new person: unimplemented")

    # Insert new person
    #
    def save_person(self, widget):
        common_name=self.common_name_text_entry.get_text()
        if not common_name:
            error_dialog = Gtk.MessageDialog(self.main_window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error: common name cannot be empty!")
            error_dialog.run()
            error_dialog.destroy()
            return
        person=Person(None, self.common_name_text_entry.get_text(), self.birth_date_text_entry.get_text(), self.birth_place_text_entry.get_text(), None)
        personDAO=PersonDAO()
        personDAO.insert(person)
        print("person added, sid is: %s" % person.sid)
        # insert person names
        # iterate over names treestore
        iter=self.namepart_treestore.get_iter_first()
        while iter:
            (person_name_role)=self.namepart_treestore.get(iter, 1)
            print("person_name_role: %s" % person_name_role)
            personName=PersonName(None, person_name_role, person.sid)
            personNameDAO=PersonNameDAO()
            personNameDAO.insert_person_name(personName)
            
            # children of name a nameparts
            if self.namepart_treestore.iter_has_child(iter):
                child_iter=self.namepart_treestore.iter_children(iter)
                while child_iter:
                    (namepart_role,namepart_value)=self.namepart_treestore.get(child_iter,1,2)                    
                    namepart=Namepart(None, namepart_role, namepart_value, personName.sid)
                    namepartDAO=NamepartDAO()
                    namepartDAO.insert_namepart(namepart)
                    child_iter=self.namepart_treestore.iter_next(child_iter)
                
            iter=self.namepart_treestore.iter_next(iter)
        get_db_connection().commit()
        print("Done")


    def get_active_name_treestore(self):
        model,tree_iter=self.nameparts_treeview.get_selection().get_selected()
        return tree_iter

    # NamePart
    def delete_name_part(self, widget):
        model,tree_iter = self.nameparts_treeview.get_selection().get_selected()
        model.remove(tree_iter)

    def add_name_part(self,widget):
        namepart_role_id,namepart_role_value=self.get_active_namepart_role()
        tree_iter=self.get_active_name_treestore()

        if tree_iter==None:
            error_dialog = Gtk.MessageDialog(self.main_window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error: name part cannot be added as root element")
            error_dialog.run()
            error_dialog.destroy()
            return

        if self.namepart_treestore.iter_depth(tree_iter)!=0:
            error_dialog = Gtk.MessageDialog(self.main_window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL, "Error: name part can be added to a root element only")
            error_dialog.run()
            error_dialog.destroy()
            return

        self.namepart_treestore.append(tree_iter,[namepart_role_id,namepart_role_value,self.namepart_role_value_entry.get_text()])
        self.namepart_role_value_entry.set_text('')
            
            
    def get_active_namepart_role(self):
        tree_iter = self.namepart_role_combobox.get_active_iter()
        if tree_iter!=None:
            model = self.namepart_role_combobox.get_model()
            name = model[tree_iter][:2]
        else:
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
