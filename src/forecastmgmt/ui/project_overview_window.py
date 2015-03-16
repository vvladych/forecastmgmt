'''
Created on 14.03.2015

@author: vvladych
'''

from gi.repository import Gtk


class ProjectOverviewWindow(Gtk.Box):
    
    def __init__(self, main_window):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.main_window=main_window
        