'''
Created on 20.08.2015

@author: vvladych
'''

from gi.repository import Gtk

from forecastmgmt.ui.ui_tools import TreeviewColumn, show_info_dialog, DateWidget, TextViewWidget
from forecastmgmt.model.publisher import Publisher



class PublicationOverviewWindow(Gtk.Grid):
    
    def __init__(self, main_window, publication=None):
        Gtk.Grid.__init__(self)
        self.main_window=main_window
        self.publication=publication
        self.create_layout()
        if publication!=None:
            self.load_publication()
        
    def create_layout(self):
        
        row=1
        
        publication_label = Gtk.Label("Publication")
        publication_label.set_justify(Gtk.Justification.LEFT)
        self.attach(publication_label,0,row,1,1)
        
        row+=1

        publisher_label = Gtk.Label("Publisher")
        publisher_label.set_justify(Gtk.Justification.LEFT)
        self.attach(publisher_label,0,row,1,1)

        self.publisher_model=self.populate_publisher_combobox_model()
        self.publisher_combobox=Gtk.ComboBox.new_with_model_and_entry(self.publisher_model)
        self.publisher_combobox.set_entry_text_column(1)
        self.attach(self.publisher_combobox,1,row,1,1)
        
        row+=1

        publication_date_label = Gtk.Label("Publication Date")
        publication_date_label.set_justify(Gtk.Justification.LEFT)
        self.attach(publication_date_label,0,row,1,1)
        
        self.publication_date_day_textentry=Gtk.Entry()
        self.publication_date_month_textentry=Gtk.Entry()
        self.publication_date_year_textentry=Gtk.Entry()
        
        publication_date_widget=DateWidget(self.publication_date_day_textentry, self.publication_date_month_textentry, self.publication_date_year_textentry)
        
        self.attach(publication_date_widget, 1,row,1,1)

        row+=1

        publication_title_label = Gtk.Label("Publication Title")
        publication_title_label.set_justify(Gtk.Justification.LEFT)
        self.attach(publication_title_label,0,row,1,1)
        
        self.publication_title_textentry=Gtk.Entry()
        self.attach(self.publication_title_textentry,1,row,2,1)


        row+=1

        publication_file_label = Gtk.Label("Publication file")
        publication_file_label.set_justify(Gtk.Justification.LEFT)
        self.attach(publication_file_label,0,row,1,1)

        self.publication_file_textentry=Gtk.Entry()
        self.attach(self.publication_file_textentry,1,row,2,1)


        row+=1

        publication_url_label = Gtk.Label("Publication URL")
        publication_url_label.set_justify(Gtk.Justification.LEFT)
        self.attach(publication_url_label,0,row,1,1)

        self.publication_url_textentry=Gtk.Entry()
        self.attach(self.publication_url_textentry,1,row,2,1)

        row+=1
        
        publication_text_label = Gtk.Label("Publication text")
        publication_text_label.set_justify(Gtk.Justification.LEFT)
        self.attach(publication_text_label,0,row,1,1)
        
        self.textview=Gtk.TextView()
        self.textview_widget=TextViewWidget(self.textview)
        self.attach(self.textview_widget,1,row,2,1)


        #self.publication_text_button=Gtk.Button("Edit text...")
        #parent_layout_grid.attach(self.publication_text_button,1,row,2,1)
        #self.publication_text_button.connect("clicked", self.edit_publication_text)
        
        row+=1
        
        self.add_publication_button=Gtk.Button("Add", Gtk.STOCK_ADD)
        self.attach(self.add_publication_button,2,row,1,1)
        self.add_publication_button.connect("clicked", self.add_publication_action)
        
        row+=1
        
        self.delete_button=Gtk.Button("Delete", Gtk.STOCK_DELETE)
        self.delete_button.connect("clicked", self.delete_action)        
        self.attach(self.delete_button,0,row,1,1)
        
        row+=1
        
    def populate_publisher_combobox_model(self):
        combobox_model=Gtk.ListStore(str,str)
        publisher_list=Publisher().get_all()
        for p in publisher_list:
            combobox_model.append(["%s" % p.sid, p.common_name])
        return combobox_model  
    
    def load_publication(self):
        self.publication_title_textentry.set_text(self.publication.title)
        self.publication_url_textentry.set_text(self.publication.publication_url)
        self.textview_widget.set_text(self.publication.publication_text)
    
    def add_publication_action(self, widget):
        print("still not implemented")
        
    def delete_action(self, widget):
        print("not implemented")
