'''
Created on 14.03.2015

@author: vvladych
'''

from gi.repository import Gtk


from forecastmgmt.ui.ui_tools import add_column_to_treeview

from forecast_originator_person_add_area import OriginatorPersonAddArea
from forecast_publication_add_area import PublicationAddArea




class ForecastOverviewWindow(Gtk.Grid):
    
    def __init__(self, main_window, forecast=None):
        Gtk.Grid.__init__(self)
        self.originatorPersonAddArea=OriginatorPersonAddArea(self, "Person", forecast)
        self.publicationAddArea=PublicationAddArea(self,"Publications", forecast)
        self.main_window=main_window
        self.forecast=forecast
        self.create_layout()
        
        
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

        row += 1
        # forecast originators
        originators_label = Gtk.Label("Originators")
        originators_label.set_justify(Gtk.Justification.LEFT)
        self.attach(originators_label,0,row,2,1)
        
        row+=1
        
        row=self.originatorPersonAddArea.create_layout(row)

        row += 1
        # project publications
        
        row=self.publicationAddArea.create_layout(row)
        
        row += 1
        # project model
        model_label = Gtk.Label("Model")
        model_label.set_justify(Gtk.Justification.LEFT)
        self.attach(model_label,0,row,2,1)
        
        self.load_forecast()
        
        
    def load_forecast(self):
        if self.forecast!=None:
            self.forecast_uuid_text_entry.set_text(self.forecast.uuid)
            
        
