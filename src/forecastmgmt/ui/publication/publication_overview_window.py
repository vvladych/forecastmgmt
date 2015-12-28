'''
Created on 20.08.2015

@author: vvladych
'''

from gi.repository import Gtk

from src.forecastmgmt.ui.ui_tools import TreeviewColumn, show_info_dialog, DateWidget, TextViewWidget
from src.forecastmgmt.model.publisher import Publisher
from src.forecastmgmt.model.publication import Publication
import datetime


class PublicationOverviewWindow(Gtk.Grid):
    
    def __init__(self, main_window, publication=None, callback=None):
        Gtk.Grid.__init__(self)
        self.main_window=main_window
        self.publication=publication
        self.create_layout()
        if publication!=None:
            self.load_publication()
        self.parent_callback=callback
        
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
        
        self.publication_date_widget=DateWidget(self.publication_date_day_textentry, self.publication_date_month_textentry, self.publication_date_year_textentry)
        
        self.attach(self.publication_date_widget, 1,row,1,1)

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

        
        row+=1
        
        self.save_publication_button=Gtk.Button("Save", Gtk.STOCK_SAVE)
        self.attach(self.save_publication_button,1,row,1,1)
        self.save_publication_button.connect("clicked", self.save_publication_action)
        
        row+=1
        
        
    def populate_publisher_combobox_model(self):
        combobox_model=Gtk.ListStore(str,str)
        publisher_list=Publisher().get_all()
        for p in publisher_list:
            combobox_model.append(["%s" % p.sid, p.common_name])
        return combobox_model  
    
    def set_active_publisher(self, publisher_sid):
        model_iter=self.publisher_model.get_iter_first()
        while self.publisher_model.iter_next(model_iter):
            if "%s" % int(publisher_sid)==self.publisher_model.get_value(model_iter,0):
                self.publisher_combobox.set_active_iter(model_iter)
            model_iter=self.publisher_model.iter_next(model_iter)
        
        
    
    def load_publication(self):
        self.publication_title_textentry.set_text(self.publication.title)
        self.publication_url_textentry.set_text("%s" % self.publication.publication_url)
        self.textview_widget.set_text(self.publication.publication_text)
        self.publication_date_widget.set_date_from_string("%s" % self.publication.publishing_date)
        self.publisher_combobox.set_active_id("%s" % self.publication.publisher_sid)
        self.set_active_publisher(self.publication.publisher_sid)

    
    def save_publication_action(self, widget):
        if self.publication!=None:
            print("update")
        else:
            self.insert_new_publication_from_mask()
            
    def insert_new_publication_from_mask(self):
        publisher_sid=self.get_active_publisher()
        publication_title=self.publication_title_textentry.get_text()
        publication_text=self.textview_widget.get_textview_text()
        publication_url=self.publication_url_textentry.get_text()
                
        # insert publication
        publication=Publication(None, None, publisher_sid, datetime.date(
                                                                         int(self.publication_date_year_textentry.get_text()),
                                                                         int(self.publication_date_month_textentry.get_text()),
                                                                         int(self.publication_date_day_textentry.get_text())), 
                                publication_title,
                                publication_url,
                                publication_text)
        publication.insert()
        show_info_dialog("Publication inserted")
        self.parent_callback()
        
        
    def get_active_publisher(self):
        tree_iter = self.publisher_combobox.get_active_iter()
        if tree_iter!=None:
            model = self.publisher_combobox.get_model()
            publisher_sid = model[tree_iter][:2]
            return publisher_sid[0]
        else:
            print("please choose a publisher!")
        
        
    def delete_action(self, widget):
        print("not implemented")
