'''
Created on 04.05.2015

@author: vvladych
'''
from gi.repository import Gtk

from masterdata_abstract_window import MasterdataAbstractWindow

from fc_object_add_mask import FCObjectAddMask
from fc_object_list_mask import FCObjectListMask

class FCObjectWindow(MasterdataAbstractWindow):

    def __init__(self, main_window):
        super(FCObjectWindow, self).__init__(main_window, FCObjectListMask(), FCObjectAddMask(main_window, self.add_working_area))
        self.specific_name="Forecast Object"
    
        
       
