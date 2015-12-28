'''
Created on 27.05.2015

@author: vvladych
'''
from gi.repository import Gtk

from src.forecastmgmt.ui.forecast.rawtext_process_component import RawTextProcessComponent

class RawTextAddDialog(Gtk.Dialog):
    
    def __init__(self, parent, forecast):
        Gtk.Dialog.__init__(self, "Text model Dialog", None, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        
        self.set_default_size(150, 400)
        self.layout_grid=Gtk.Grid()
        
        self.forecast=forecast
        
        self.process_component=RawTextProcessComponent(forecast)
        
        self.create_layout()
        self.show_all()
        
        
    def create_layout(self):
        box = self.get_content_area()
        
        box.add(self.layout_grid)
        
        row = 0
        label = Gtk.Label("Forecast model(s)")
        self.layout_grid.attach(label,0,row,1,1)
        
        row+=3
        row=self.process_component.create_layout(self.layout_grid, row)
        
        return row            
    
        
        
        
