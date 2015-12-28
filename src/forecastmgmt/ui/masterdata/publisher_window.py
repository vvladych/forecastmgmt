'''
Created on 04.05.2015

@author: vvladych
'''
from gi.repository import Gtk

from src.forecastmgmt.ui.masterdata.masterdata_abstract_window import MasterdataAbstractWindow

from src.forecastmgmt.ui.masterdata.publisher_add_mask import PublisherAddMask
from src.forecastmgmt.ui.masterdata.publisher_list_mask import PublisherListMask

class PublisherWindow(MasterdataAbstractWindow):

    def __init__(self, main_window):
        super(PublisherWindow, self).__init__(main_window, PublisherListMask(), PublisherAddMask(main_window, self.add_working_area))
    
        
       
