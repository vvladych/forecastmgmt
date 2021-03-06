'''
Created on 21.03.2015

@author: vvladych
'''

from forecastmgmt.model.fc_project import FcProject
from forecastmgmt.ui.ui_tools import TextViewWidget

from gi.repository import Gtk

class ForecastNewDialog(Gtk.Dialog):
    
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Create new forecast", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        
        self.set_default_size(400, 400)
        
        self.__create_ui()
        self.show_all()
        
    def perform_insert(self):
        
        project=FcProject(common_name=self.project_name_text_entry.get_text(), short_description=self.__get_desc_text())
        project.insert()
        
    
    def __get_desc_text(self):
        textbuffer=self.desc_textview.get_buffer()
        short_desc=textbuffer.get_text(textbuffer.get_start_iter(),textbuffer.get_end_iter(),True)
        return short_desc
        
    def __create_ui(self):
        box = self.get_content_area()
        
        layout_grid=Gtk.Grid()
        
        box.add(layout_grid)
        
        row = 0
        label = Gtk.Label("Create a new project")
        layout_grid.attach(label,0,row,1,1)
        
        row+=1
        project_name_label = Gtk.Label("Project name")
        project_name_label.set_justify(Gtk.Justification.LEFT)
        layout_grid.attach(project_name_label,0,row,1,1)
        self.project_name_text_entry=Gtk.Entry()
        layout_grid.attach(self.project_name_text_entry,1,row,1,1)        
        
        row+=1
        project_desc_label = Gtk.Label("Short description")
        project_desc_label.set_justify(Gtk.Justification.LEFT)
        layout_grid.attach(project_desc_label,0,row,1,1)
        self.desc_textview=Gtk.TextView()
        textview_widget=TextViewWidget(self.desc_textview)
                
        layout_grid.attach(textview_widget,1,row,1,1)        
        
        
        
        
