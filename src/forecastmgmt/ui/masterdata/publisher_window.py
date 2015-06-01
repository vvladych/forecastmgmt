'''
Created on 04.05.2015

@author: vvladych
'''
from gi.repository import Gtk

from masterdata_abstract_window import MasterdataAbstractWindow

from publisher_add_mask import PublisherAddMask
from publisher_list_mask import PublisherListMask

class PublisherWindow(MasterdataAbstractWindow):

    def __init__(self, main_window):
        super(PublisherWindow, self).__init__(main_window, PublisherListMask(), PublisherAddMask(main_window, self.add_working_area))
    
        
       
