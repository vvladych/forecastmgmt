'''
Created on 26.04.2015

@author: vvladych
'''
from gi.repository import Gtk

from masterdata_abstract_window import MasterdataAbstractWindow


class OrganisationWindow(MasterdataAbstractWindow):

    def __init__(self, main_window):
        super(OrganisationWindow, self).__init__(main_window)
        self.add_working_area(None, "list")
        
        
        
    def add_working_area(self, widget, action="list"):
        self.clean_working_area_box()
        self.clean_action_area_box()
        self.create_action_area()
        if action=="list":
            print("hier in list")
        self.working_area.show_all()   

                
    def delete_action(self,widget,callback):
        print("in delete organisation")

