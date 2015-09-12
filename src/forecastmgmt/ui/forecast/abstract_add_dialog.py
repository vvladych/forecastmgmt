'''
Created on 13.09.2015

@author: vvladych
'''

from gi.repository import Gtk

class AbstractAddDialog(Gtk.Dialog):
    
    def __init__(self, parent, forecast, dialog_title, process_component):
        Gtk.Dialog.__init__(self, dialog_title, None, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        
        self.dialog_title=dialog_title
        
        self.set_default_size(150, 400)
        self.layout_grid=Gtk.Grid()
        
        self.forecast=forecast
        
        self.process_component=process_component
        
        self.create_layout()
        self.show_all()

        
    def create_layout(self):
        box = self.get_content_area()
        
        box.add(self.layout_grid)
        
        row = 0
        label = Gtk.Label(self.dialog_title)
        self.layout_grid.attach(label,0,row,1,1)
        
        row+=3
        row=self.process_component.create_layout(self.layout_grid, row)
        
        return row            
        