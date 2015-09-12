'''
Created on 03.05.2015

@author: vvladych
'''
from gi.repository import Gtk



from forecastmgmt.model.person import Person
from forecastmgmt.model.person_namepart import Namepart
from forecastmgmt.dao.dao_utils import enum_retrieve_valid_values
from forecastmgmt.model.personrole import Personrole

from forecastmgmt.ui.masterdata.personrole_add_dialog import PersonroleAddDialog


from forecastmgmt.ui.ui_tools import add_column_to_treeview, DateWidget
import datetime

from masterdata_abstract_window import AbstractAddMask

class PersonAddMask(AbstractAddMask):

    def __init__(self, main_window, reset_callback=None):
        super(PersonAddMask, self).__init__(main_window, reset_callback)
        
        
    def create_layout(self):
        self.set_column_spacing(5)
        self.set_row_spacing(3)

        placeholder_label = Gtk.Label("")
        placeholder_label.set_size_request(1,40)
        self.attach(placeholder_label,0,-1,1,1)

        row = 0
        # Row 0: person uuid
        self.add_uuid_row("Person UUID", row)
        
        row+=1
        # Row 1: common name
        self.add_common_name_row("Common Name", row)
        
        row+=1
        # Row: birth date
        birth_date_label = Gtk.Label("Birth Date")
        self.attach(birth_date_label,0,row,1,1)
        
        
        self.birth_date_day_text_entry=Gtk.Entry()
        self.birth_date_month_text_entry=Gtk.Entry()
        self.birth_date_year_text_entry=Gtk.Entry()
        self.attach(DateWidget(self.birth_date_day_text_entry,self.birth_date_month_text_entry,self.birth_date_year_text_entry),1,row,1,1)
        row+=1
        
        
        # Row: birth place
        birth_place_label = Gtk.Label("Birth Place")
        self.attach(birth_place_label,0,row,1,1)
        self.birth_place_text_entry=Gtk.Entry()
        self.attach(self.birth_place_text_entry,1,row,1,1)

        row+=1
        
        # name 
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

        
        row+=1
        # name part role
        namepart_label = Gtk.Label("Name part")
        self.attach(namepart_label,0,row,1,1)

        namepart_add_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        namepart_add_button.connect("clicked", self.add_name_part) 
        self.attach(namepart_add_button,2,row,1,1)

        namepart_delete_button = Gtk.Button("Delete", Gtk.STOCK_DELETE)
        namepart_delete_button.connect("clicked", self.delete_name_part) 
        self.attach(namepart_delete_button,3,row,1,1)

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
        namepart_scrolledwindow=Gtk.ScrolledWindow()
        namepart_scrolledwindow.set_hexpand(True)
        namepart_scrolledwindow.set_vexpand(True)
        namepart_scrolledwindow.add(self.nameparts_treeview)
        self.attach(namepart_scrolledwindow,0,row,4,1)
        
        
        row+=1
                
        # Person roles
        personrole_label = Gtk.Label("Person role")
        self.attach(personrole_label,0,row,1,1)
        
        
        self.personroles_model=Gtk.ListStore(int,str)

        self.populate_personroles_model()
        self.personroles_combobox=Gtk.ComboBox.new_with_model_and_entry(self.personroles_model)
        self.personroles_combobox.set_entry_text_column(1)
        self.personroles_combobox.set_active(0)
        self.attach(self.personroles_combobox,1,row,1,1)
        
        personrole_add_button = Gtk.Button("Add", Gtk.STOCK_ADD)
        personrole_add_button.connect("clicked", self.add_personrole)
        self.attach(personrole_add_button,2,row,1,1)
        

        personrole_manage_button = Gtk.Button("Manage...")
        personrole_manage_button.connect("clicked", self.manage_personrole)
        self.attach(personrole_manage_button,3,row,1,1)
        
        row+=1

        # Person roles
        personrole_start_date_label = Gtk.Label("From")
        self.attach(personrole_start_date_label,0,row,1,1)
        
        self.personrole_start_day_text_entry=Gtk.Entry()
        self.personrole_start_month_text_entry=Gtk.Entry()
        self.personrole_start_year_text_entry=Gtk.Entry()
        self.attach(DateWidget(self.personrole_start_day_text_entry,self.personrole_start_month_text_entry,self.personrole_start_year_text_entry),1,row,1,1)
        row+=1

        personrole_end_date_label = Gtk.Label("To")
        self.attach(personrole_end_date_label,0,row,1,1)

        self.personrole_end_day_text_entry=Gtk.Entry()
        self.personrole_end_month_text_entry=Gtk.Entry()
        self.personrole_end_year_text_entry=Gtk.Entry()
        self.attach(DateWidget(self.personrole_end_day_text_entry,self.personrole_end_month_text_entry,self.personrole_end_year_text_entry),1,row,1,1)
        row+=1

        
        self.create_personrole_treeview()
        personrole_scrolledwindow=Gtk.ScrolledWindow()
        personrole_scrolledwindow.set_hexpand(True)
        personrole_scrolledwindow.set_vexpand(True)
        personrole_scrolledwindow.add(self.personrole_treeview)
        self.attach(personrole_scrolledwindow,0,row,4,1)

        row+=1
        # Row 5
        save_button = Gtk.Button("Save", Gtk.STOCK_SAVE)
        save_button.connect("clicked", self.save_current_object)
        self.attach(save_button,1,row,1,1)

        back_button = Gtk.Button("Back", Gtk.STOCK_GO_BACK)
        back_button.connect("clicked", self.parent_callback_func, self.reset_callback)
        self.attach(back_button,2,row,1,1)
        
                
    def fill_mask_from_current_object(self):
        if self.current_object!=None:
            self.uuid_text_entry.set_text(self.current_object.uuid)
            self.common_name_text_entry.set_text(self.current_object.common_name)
            self.birth_place_text_entry.set_text(self.current_object.birth_place)
            if self.current_object.birth_date!=None:
                self.birth_date_year_text_entry.set_text("%s" % self.current_object.birth_date.year)
                self.birth_date_month_text_entry.set_text("%s" % self.current_object.birth_date.month)
                self.birth_date_day_text_entry.set_text("%s" % self.current_object.birth_date.day)
            self.namepart_treestore.clear()
            for name in self.current_object.names:
                tree_iter=self.namepart_treestore.append(None,[name.sid, name.name_role, None])
                for namepart in name.nameparts:
                    self.namepart_treestore.append(tree_iter,[namepart.sid, namepart.namepart_role, namepart.namepart_value])
            self.personrole_treestore.clear()
            for personrole in self.current_object.personroles:
                roleview=Personrole(sid=personrole.personrole_sid)
                roleview.load()
                self.personrole_treestore.append(None,[personrole.personrole_sid,roleview.common_name,None])
        else:
            self.uuid_text_entry.set_text("")
            self.common_name_text_entry.set_text("")
            self.birth_place_text_entry.set_text("")
            self.birth_date_day_text_entry.set_text("")
            self.birth_date_month_text_entry.set_text("")
            self.birth_date_year_text_entry.set_text("")
            self.namepart_treestore.clear()
            self.personrole_treestore.clear()


    def add_name(self,widget):
        name_role_id,name_role_value = self.get_active_name_role()
        self.namepart_treestore.append(None,[name_role_id,name_role_value,None])
        
    def add_personrole(self, widget):
        (personrole_id,personrole)=self.get_active_personrole()
        self.personrole_treestore.append(None,[personrole_id,personrole,None])
        
    def manage_personrole(self, widget):
        personroleDialog=PersonroleAddDialog(self, self.refresh_personroles_model())
        personroleDialog.run()
        personroleDialog.destroy()
        self.refresh_personroles_model()


    def get_active_name_role(self):
        name_combobox_iter = self.name_role_combobox.get_active_iter()
        if name_combobox_iter!=None:
            model = self.name_roles_model
            name = model[name_combobox_iter][:2]
        else:
            name=self.name_role_combobox.get_child()
        return name

     
    def __get_birth_date_from_mask(self):
        if (self.birth_date_day_text_entry.get_text()!='' and self.birth_date_month_text_entry.get_text()!='' and self.birth_date_year_text_entry.get_text()!=''):
            return datetime.date(int(self.birth_date_year_text_entry.get_text()), 
                                int(self.birth_date_month_text_entry.get_text()), 
                                int(self.birth_date_day_text_entry.get_text()))
        return None 
                   
            
    def create_object_from_mask(self):
        common_name=self.common_name_text_entry.get_text()
        if not common_name:
            self.show_error_dialog("Error: common name cannot be empty!")
            return
        
        person_sid=None
        
        person=Person(person_sid, 
                      self.common_name_text_entry.get_text(), 
                      self.__get_birth_date_from_mask(),
                      self.birth_place_text_entry.get_text(),
                      self.uuid_text_entry.get_text())

        self.__read_person_names_from_mask(person)
        self.__read_personroles_from_mask(person)

        if self.current_object!=None:
            person_sid=self.current_object.sid
        
        return person
    
    
    def __read_person_names_from_mask(self, person):
        # insert person names
        # iterate over names treestore
        name_iter=self.namepart_treestore.get_iter_first()
        while name_iter:
            (person_name_sid, person_name_role)=self.namepart_treestore.get(name_iter, 0, 1)
            
            namepart_list=[]
            # children of name a nameparts
            if self.namepart_treestore.iter_has_child(name_iter):
                child_iter=self.namepart_treestore.iter_children(name_iter)
                while child_iter:
                    (namepart_sid,namepart_role,namepart_value)=self.namepart_treestore.get(child_iter,0,1,2)                    
                    namepart=Namepart(namepart_sid, namepart_role, namepart_value, person_name_sid)
                    namepart_list.append(namepart)
                    child_iter=self.namepart_treestore.iter_next(child_iter)
            
            person.add_name(person_name_sid, person_name_role, self.current_object.sid, namepart_list)
            name_iter=self.namepart_treestore.iter_next(name_iter)
            
        
    def __read_personroles_from_mask(self, person):
        personrole_iter=self.personrole_treestore.get_iter_first()
        
        while personrole_iter:
            (personrole_sid)=self.personrole_treestore[personrole_iter][0]
            person.add_personrole(personrole_sid)
            personrole_iter=self.personrole_treestore.iter_next(personrole_iter)
        

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
        self.nameparts_treeview.append_column(add_column_to_treeview("id", 0, True))
        self.nameparts_treeview.append_column(add_column_to_treeview("Role", 1, False))
        self.nameparts_treeview.append_column(add_column_to_treeview("Value", 2, False))
        self.nameparts_treeview.set_size_request(200,200)
        self.nameparts_treeview.connect("row-activated", self.on_namepart_row_selection)

    def on_namepart_row_selection(self,treeview,path,column):
        model,treeiter=self.nameparts_treeview.get_selection().get_selected()
        self.namepart_role_combobox.set_active(model[treeiter][0])
        self.namepart_role_value_entry.set_text(model[treeiter][2])
        
        
    def create_personrole_treeview(self):
        self.personrole_treestore = Gtk.TreeStore(int,str,str)
        self.personrole_treeview = Gtk.TreeView(self.personrole_treestore)
        self.personrole_treeview.append_column(add_column_to_treeview("id", 0, True))
        self.personrole_treeview.append_column(add_column_to_treeview("Role", 1, False))
        self.personrole_treeview.append_column(add_column_to_treeview("Date", 2, False))
        self.personrole_treeview.set_size_request(200,200)
        

    def populate_namepart_roles_model(self):
        namepart_roles_model = Gtk.ListStore(int, str)
        namepart_roles_list=enum_retrieve_valid_values("t_person_name_part_role")
        counter=0
        for namepart_role in namepart_roles_list:
            namepart_roles_model.append([counter,namepart_role])
            counter+=1
        return namepart_roles_model
    

    def populate_name_roles_model(self):
        name_roles_model = Gtk.ListStore(int,str)
        counter=0
        nameroles_list = enum_retrieve_valid_values("t_person_name_role")
        for namerole in nameroles_list:
            name_roles_model.append([counter,namerole])
            counter+=1
        return name_roles_model

    def refresh_personroles_model(self):
        self.personroles_model.clear()
        self.populate_personroles_model()
        


    def populate_personroles_model(self):
        personroles = Personrole().get_all()
        for personrole in personroles:
            self.personroles_model.append([personrole.sid,personrole.common_name])
            
    def get_active_personrole(self):
        personrole_combobox_iter = self.personroles_combobox.get_active_iter()
        if personrole_combobox_iter!=None:
            personrole = self.personroles_model[personrole_combobox_iter][:2]
            print(personrole)
        return personrole
        

