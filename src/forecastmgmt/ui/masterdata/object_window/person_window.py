from gi.repository import Gtk

from masterdata_abstract_window import MasterdataAbstractWindow

from forecastmgmt.ui.masterdata.object_add_mask.person_add_mask import PersonAddMask
from forecastmgmt.ui.masterdata.object_list_mask.person_list_mask import PersonListMask

class PersonWindow(MasterdataAbstractWindow):

    def __init__(self, main_window):
        super(PersonWindow, self).__init__(main_window, PersonListMask(), PersonAddMask(main_window, self.add_working_area))
    
        
        
        
        
