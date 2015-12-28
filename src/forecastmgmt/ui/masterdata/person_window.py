from gi.repository import Gtk

from src.forecastmgmt.ui.masterdata.masterdata_abstract_window import MasterdataAbstractWindow

from src.forecastmgmt.ui.masterdata.person_add_mask import PersonAddMask
from src.forecastmgmt.ui.masterdata.person_list_mask import PersonListMask

class PersonWindow(MasterdataAbstractWindow):

    def __init__(self, main_window):
        super(PersonWindow, self).__init__(main_window, PersonListMask(), PersonAddMask(main_window, self.add_working_area))
    
        
        
        
        
