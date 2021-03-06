'''
Created on 14.03.2015

@author: vvladych
'''

from gi.repository import Gtk

from publication_add_dialog import PublicationAddDialog
from publication_process_component import PublicationOverviewComponent
from originator_add_dialog import OriginatorAddDialog
from originator_process_component import OriginatorOverviewComponent
from rawtext_add_dialog import RawTextAddDialog
from model_add_dialog import ModelAddDialog
from textmodel_add_dialog import TextModelAddDialog
from forecastmgmt.ui.ui_tools import TextViewWidget


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
        uuid_label.set_justify(Gtk.Justification.RIGHT)
        self.attach(uuid_label,0,row,1,1)
        self.forecast_uuid_text_entry=Gtk.Entry()
        self.forecast_uuid_text_entry.set_editable(False)
        self.attach(self.forecast_uuid_text_entry,1,row,1,1)
        
        if self.forecast!=None:
            self.forecast_uuid_text_entry.set_text(self.forecast.uuid)

        row += 1
        
        description_label=Gtk.Label("Description")
        description_label.set_justify(Gtk.Justification.RIGHT)
        self.attach(description_label,0,row,1,1)
        
        short_desc_text=None
        if self.forecast!=None:
            short_desc_text=self.forecast.short_description                
        
        self.desc_textview=Gtk.TextView()
        desc_textview_widget=TextViewWidget(self.desc_textview, short_desc_text)
        
        self.attach(desc_textview_widget,1,row,1,1)
        
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
        self.attach(model_label,0,row,3,1)
        
        row += 1

        buttonGrid=Gtk.Grid()
        
        button_rawtext_dialog=Gtk.Button("Raw text")
        button_rawtext_dialog.connect("clicked", self.show_rawtext_dialog)
        buttonGrid.attach(button_rawtext_dialog,0,row,1,1)

        button_edit_textmodel_dialog=Gtk.Button("Text model(s)")
        button_edit_textmodel_dialog.connect("clicked", self.show_textmodel_dialog)
        buttonGrid.attach(button_edit_textmodel_dialog,1,row,1,1)


        button_edit_model_dialog=Gtk.Button("Formal model(s)")
        button_edit_model_dialog.connect("clicked", self.show_model_dialog)
        buttonGrid.attach(button_edit_model_dialog,2,row,1,1)
        
        self.attach(buttonGrid,0,row,2,1)

        
    
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
    
        
    def show_rawtext_dialog(self, widget):
        dialog=RawTextAddDialog(self, self.forecast)
        dialog.run()
        dialog.destroy()

    def show_model_dialog(self, widget):
        dialog=ModelAddDialog(self, self.forecast)
        dialog.run()
        dialog.destroy()
    
    def show_textmodel_dialog(self, widget):
        dialog=TextModelAddDialog(self, self.forecast)
        dialog.run()
        dialog.destroy()
        
