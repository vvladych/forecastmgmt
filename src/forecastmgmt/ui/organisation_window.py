'''
Created on 26.04.2015

@author: vvladych
'''
from gi.repository import Gtk

from masterdata_abstract_window import MasterdataAbstractWindow
from organisation_list_mask import OrganisationListMask


class OrganisationWindow(MasterdataAbstractWindow):

    def __init__(self, main_window):
        super(OrganisationWindow, self).__init__(main_window,OrganisationListMask())
