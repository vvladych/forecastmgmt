'''
Created on 02.05.2015

@author: vvladych
'''
from gi.repository import Gtk
from masterdata_abstract_window import AbstractListMask
from forecastmgmt.model.person import Person

class PersonListMask(AbstractListMask):

    treeview_columns=[{"column":"common name","hide":False},{"column":"birth date","hide":False},{"column":"birth place","hide":False},
                      {"column":"person uuid","hide":False},{"column":"person_sid","hide":True}]


    def __init__(self):
        super(PersonListMask, self).__init__(PersonListMask.treeview_columns)        
                

    def populate_object_view_table(self):
        self.store.clear()
        persons = Person().get_all()
        for person in persons:
            self.store.append(["%s" % person.common_name, "%s" % person.birth_date, "%s" % person.birth_place, "%s" % person.uuid, "%s" % person.sid])
        

    def delete_object(self):
        model,tree_iter = self.tree.get_selection().get_selected()
        (person_sid)=model.get(tree_iter, 4)
        Person(person_sid).delete()
        model.remove(tree_iter)
            
    def get_current_object(self):
        model,tree_iter = self.tree.get_selection().get_selected()
        (person_sid)=model.get(tree_iter, 4)
        return Person(person_sid)

    def on_row_select(self,widget,path,data):
        print("on_row_select")