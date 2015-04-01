'''
Created on 14.03.2015

@author: vvladych
'''

from gi.repository import Gtk


class ProjectOverviewWindow(Gtk.Grid):
    
    def __init__(self, main_window, forecast=None):
        Gtk.Grid.__init__(self)
        self.main_window=main_window
        self.create_layout()
        self.load_forecast(forecast)
        
        
    def create_layout(self):
        self.set_column_spacing(5)
        self.set_row_spacing(3)

        placeholder_label = Gtk.Label("")
        placeholder_label.set_size_request(1,40)
        self.attach(placeholder_label,0,-1,1,1)

        row = 0
        # Row 0: project uuid
        uuid_label = Gtk.Label("forecast UUID")
        uuid_label.set_justify(Gtk.Justification.LEFT)
        self.attach(uuid_label,0,row,1,1)
        self.forecast_uuid_text_entry=Gtk.Entry()
        self.forecast_uuid_text_entry.set_editable(False)
        self.attach(self.forecast_uuid_text_entry,1,row,1,1)
        
        
    def load_forecast(self, forecast=None):
        if forecast!=None:
            self.forecast_uuid_text_entry.set_text(forecast.forecast_uuid)
        