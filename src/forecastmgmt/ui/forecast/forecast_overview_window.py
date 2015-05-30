'''
Created on 14.03.2015

@author: vvladych
'''

from gi.repository import Gtk

#from forecast_publication_add_area import PublicationAddArea
from publication_add_dialog import PublicationAddDialog
from publication_process_component import PublicationOverviewComponent
from originator_add_dialog import OriginatorAddDialog
from originator_process_component import OriginatorOverviewComponent
from model_add_dialog import ModelAddDialog
from forecastmgmt.ui.forecast import publication_add_dialog


class ForecastOverviewWindow(Gtk.Grid):
    
    def __init__(self, main_window, forecast=None):
        Gtk.Grid.__init__(self)
        self.originator_overview_component=OriginatorOverviewComponent(forecast)
        self.publication_overview_component=PublicationOverviewComponent(forecast)
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
        
        if self.forecast!=None:
            self.forecast_uuid_text_entry.set_text(self.forecast.uuid)

        row += 1
        
        scrolledwindow= Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.desc_textview=Gtk.TextView()
        scrolledwindow.add(self.desc_textview)
        
        if self.forecast!=None:
            if self.forecast.short_description!=None:
                self.desc_textview.get_buffer().set_text(self.forecast.short_description)
            
        self.attach(scrolledwindow,0,row,1,1)
        
        row += 3
        # forecast originators
        originators_label = Gtk.Label("Originators")
        originators_label.set_justify(Gtk.Justification.LEFT)
        self.attach(originators_label,0,row,2,1)
        
        row+=1
        
        
        #row=self.originatorPersonAddArea.create_layout(row)
        self.originator_overview_component.clean_and_populate_model()
        row = self.originator_overview_component.create_layout(self, row)

        row += 1
        button_add_originator_dialog=Gtk.Button("Edit originator(s)")
        button_add_originator_dialog.connect("clicked", self.show_originator_dialog)
        self.attach(button_add_originator_dialog,0,row,1,1)
        
        row+=2


        publications_label = Gtk.Label("Publications")
        publications_label.set_justify(Gtk.Justification.LEFT)
        self.attach(publications_label,0,row,2,1)

        row+=1
        
        # project publications
        self.publication_overview_component.clean_and_populate_model()
        row = self.publication_overview_component.create_layout(self, row)
        
        row +=1 
        button_add_publication_dialog=Gtk.Button("Edit publication(s)")
        button_add_publication_dialog.connect("clicked", self.show_publication_dialog)
        self.attach(button_add_publication_dialog,0,row,1,1)
        
        
        row += 3
        # project model
        model_label = Gtk.Label("Model")
        model_label.set_justify(Gtk.Justification.LEFT)
        self.attach(model_label,0,row,2,1)
        
        row += 1

        button_edit_model_dialog=Gtk.Button("Edit Model(s)")
        button_edit_model_dialog.connect("clicked", self.show_model_dialog)
        self.attach(button_edit_model_dialog,0,row,1,1)
        
    
    def show_originator_dialog(self, widget):
        dialog=OriginatorAddDialog(self, self.forecast)
        dialog.run()
        dialog.destroy()
        self.originator_overview_component.clean_and_populate_model()
        

    def show_publication_dialog(self, widget):
        dialog=PublicationAddDialog(self, self.forecast)
        dialog.run()
        dialog.destroy()
        self.publication_overview_component.clean_and_populate_model()
    
        
    def show_model_dialog(self, widget):
        dialog=ModelAddDialog(self, self.forecast)
        dialog.run()
        dialog.destroy()
        self.publication_overview_component.clean_and_populate_model()
    

