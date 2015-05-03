'''
Created on 26.04.2015

@author: vvladych
'''
from gi.repository import Gtk

from masterdata_abstract_window import MasterdataAbstractWindow
from organisation_list_mask import OrganisationListMask


class OrganisationWindow(MasterdataAbstractWindow):

    def __init__(self, main_window):
        super(OrganisationWindow, self).__init__(main_window)
        self.add_working_area(None, "list")
        
        
    def add_working_area(self, widget, action="list"):
        self.recreate_working_area()
        if action=="list":
            self.organisationListMask=OrganisationListMask()
            self.working_area.pack_start(self.organisationListMask, False, False, 0)
        self.working_area.show_all()

                
    def delete_action(self,widget,callback):
        print("in delete organisation")

