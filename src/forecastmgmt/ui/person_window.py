from gi.repository import Gtk

from masterdata_abstract_window import MasterdataAbstractWindow

from person_add_mask import PersonAddMask
from person_list_mask import PersonListMask

class PersonWindow(MasterdataAbstractWindow):

    def __init__(self, main_window):
        super(PersonWindow, self).__init__(main_window, PersonListMask(), PersonAddMask(main_window, self.add_working_area))
    
        
        
        
        
