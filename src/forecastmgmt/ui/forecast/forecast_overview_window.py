'''
Created on 14.03.2015

@author: vvladych
'''

from gi.repository import Gtk

from forecast_publication_add_area import PublicationAddArea
from originator_add_dialog import OriginatorAddDialog
from originator_process_component import OriginatorOverviewComponent


class ForecastOverviewWindow(Gtk.Grid):
    
    def __init__(self, main_window, forecast=None):
        Gtk.Grid.__init__(self)
        self.originator_overview_component=OriginatorOverviewComponent(forecast)
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
        
        row+=2
        
        
        #row=self.originatorPersonAddArea.create_layout(row)
        self.originator_overview_component.clean_and_populate_model()
        row = self.originator_overview_component.create_layout(self, row)

        row += 1
        button_add_originator_dialog=Gtk.Button("Edit originator(s)")
        button_add_originator_dialog.connect("clicked", self.show_add_originator_dialog)
        self.attach(button_add_originator_dialog,0,row,1,1)
        
        row+=2

        
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
            
    def show_add_originator_dialog(self, widget):
        dialog=OriginatorAddDialog(self, self.forecast)
        dialog.run()
        dialog.destroy()
        self.originator_overview_component.clean_and_populate_model()
