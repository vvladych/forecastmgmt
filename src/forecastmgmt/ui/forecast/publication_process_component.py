'''
Created on 20.05.2015

@author: vvladych
'''
from gi.repository import Gtk

from forecastmgmt.ui.forecast.abstract_data_process_component import AbstractDataOverviewComponent, AbstractDataManipulationComponent, AbstractDataProcessComponent 

from forecastmgmt.ui.ui_tools import TreeviewColumn, show_info_dialog, DateWidget, TextViewWidget

from forecastmgmt.dao.db_connection import get_db_connection
import psycopg2.extras


import datetime

from forecastmgmt.model.publisher import Publisher
from forecastmgmt.model.publication import Publication
from forecastmgmt.model.forecast_publication import ForecastPublication



class PublicationProcessComponent(AbstractDataProcessComponent):
    
    def __init__(self, forecast):
        super(PublicationProcessComponent, self).__init__(PublicationManipulationComponent(forecast, PublicationOverviewComponent(forecast)))
        
        
class PublicationManipulationComponent(AbstractDataManipulationComponent):
    
    def __init__(self, forecast, overview_component):
        super(PublicationManipulationComponent, self).__init__(overview_component)
        self.forecast=forecast
        
    def create_layout(self, parent_layout_grid, row):
        
        publication_label = Gtk.Label("Publication")
        publication_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(publication_label,0,row,1,1)
        
        row+=1

        publisher_label = Gtk.Label("Publisher")
        publisher_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(publisher_label,0,row,1,1)

        self.publisher_model=self.populate_publisher_combobox_model()
        self.publisher_combobox=Gtk.ComboBox.new_with_model_and_entry(self.publisher_model)
        self.publisher_combobox.set_entry_text_column(1)
        parent_layout_grid.attach(self.publisher_combobox,1,row,1,1)
        
        row+=1

        publication_date_label = Gtk.Label("Publication Date")
        publication_date_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(publication_date_label,0,row,1,1)
        
        self.publication_date_day_textentry=Gtk.Entry()
        self.publication_date_month_textentry=Gtk.Entry()
        self.publication_date_year_textentry=Gtk.Entry()
        
        publication_date_widget=DateWidget(self.publication_date_day_textentry, self.publication_date_month_textentry, self.publication_date_year_textentry)
        
        parent_layout_grid.attach(publication_date_widget, 1,row,1,1)

        row+=1

        publication_title_label = Gtk.Label("Publication Title")
        publication_title_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(publication_title_label,0,row,1,1)
        
        self.publication_title_textentry=Gtk.Entry()
        parent_layout_grid.attach(self.publication_title_textentry,1,row,2,1)


        row+=1

        publication_file_label = Gtk.Label("Publication file")
        publication_file_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(publication_file_label,0,row,1,1)

        self.publication_file_textentry=Gtk.Entry()
        parent_layout_grid.attach(self.publication_file_textentry,1,row,2,1)


        row+=1
        
        publication_text_label = Gtk.Label("Publication text")
        publication_text_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(publication_text_label,0,row,1,1)
        
        self.textview=Gtk.TextView()
        self.textview_widget=TextViewWidget(self.textview)
        parent_layout_grid.attach(self.textview_widget,1,row,2,1)


        #self.publication_text_button=Gtk.Button("Edit text...")
        #parent_layout_grid.attach(self.publication_text_button,1,row,2,1)
        #self.publication_text_button.connect("clicked", self.edit_publication_text)
        
        row+=1
        
        self.add_publication_button=Gtk.Button("Add", Gtk.STOCK_ADD)
        parent_layout_grid.attach(self.add_publication_button,2,row,1,1)
        self.add_publication_button.connect("clicked", self.add_publication_action)
        
        row+=1
        
        self.delete_button=Gtk.Button("Delete", Gtk.STOCK_DELETE)
        self.delete_button.connect("clicked", self.delete_action)        
        parent_layout_grid.attach(self.delete_button,0,row,1,1)
        
        row+=1
        
        row=self.overview_component.create_layout(parent_layout_grid, row)
        
        row+=2
        
        return row
        
    def populate_publisher_combobox_model(self):
        combobox_model=Gtk.ListStore(str,str)
        publisher_list=Publisher().get_all()
        for p in publisher_list:
            combobox_model.append(["%s" % p.sid, p.common_name])
        return combobox_model
    
    
    def add_publication_action(self, widget):
        # get publisher sid
        publisher_sid=self.get_active_publisher()
        publication_title=self.publication_title_textentry.get_text()
        publication_text=self.textview_widget.get_textview_text()
                
        # insert publication
        publication=Publication(None, None, publisher_sid, datetime.date(
                                                                         int(self.publication_date_year_textentry.get_text()),
                                                                         int(self.publication_date_month_textentry.get_text()),
                                                                         int(self.publication_date_day_textentry.get_text())), 
                                publication_title,
                                publication_text)
        publication.insert()
        
        # insert forecast_originator
        forecast_publication = ForecastPublication(forecast_sid=self.forecast.sid, publication_sid=publication.sid)
        forecast_publication.insert()
        
        show_info_dialog("Add successful")
        self.overview_component.clean_and_populate_model()
        

    def get_active_publisher(self):
        tree_iter = self.publisher_combobox.get_active_iter()
        if tree_iter!=None:
            model = self.publisher_combobox.get_model()
            publisher_sid = model[tree_iter][:2]
            return publisher_sid[0]
        else:
            print("please choose a publisher!")

    
    
    def delete_action(self, widget):
        model,tree_iter = self.overview_component.treeview.get_selection().get_selected()
        (publication_sid)=model.get(tree_iter, 0)
        Publication(publication_sid).delete()
        model.remove(tree_iter)   
        show_info_dialog("Delete successful")   
        
    
    def edit_publication_text(self, widget):
        dialog=PublicationTextDialog(None)
        dialog.run()
        dialog.destroy()    
        

class PublicationOverviewComponent(AbstractDataOverviewComponent):
    
    treecolumns=[TreeviewColumn("publication_sid", 0, True), TreeviewColumn("publisher_sid", 1, True), 
                 TreeviewColumn("Publisher", 2, False), TreeviewColumn("Title", 3, False, True),
                 TreeviewColumn("Date", 4, False), TreeviewColumn("Publication text", 5, True)]
    
    def __init__(self, forecast):
        self.forecast=forecast
        super(PublicationOverviewComponent, self).__init__(PublicationOverviewComponent.treecolumns)
        

    def populate_model(self):
        self.treemodel.clear()
        cur=get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        data=(self.forecast.sid,)
        cur.execute("""SELECT 
                        fc_publication.sid as publication_sid, fc_publisher.sid as publisher_sid, 
                        fc_publisher.publisher_common_name, fc_publication.title, fc_publication.publishing_date,
                        fc_publication.publication_text   
                        FROM 
                        fc_forecast_publication, fc_publication, fc_publisher 
                        WHERE
                        fc_forecast_publication.forecast_sid=%s AND
                        fc_forecast_publication.publication_sid=fc_publication.sid AND  
                        fc_publication.publisher_sid=fc_publisher.sid 
                        """,data)
        for p in cur.fetchall():
            self.treemodel.append([ "%s" % p.publication_sid, "%s" % p.publisher_sid, p.publisher_common_name, p.title, p.publishing_date.strftime('%d.%m.%Y'),p.publication_text])
        cur.close()
        
        

class PublicationTextDialog(Gtk.Dialog):
    
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Publication text dialog", None, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        
        self.set_default_size(150, 400)
        self.layout_grid=Gtk.Grid()
                
        self.create_layout()
        self.show_all()   
         
    def create_layout(self):
        box = self.get_content_area()
        
        box.add(self.layout_grid)
        
        row = 0
        label = Gtk.Label("Publication text")
        self.layout_grid.attach(label,0,row,1,1)
        
        self.textview=Gtk.TextView()
        textview_widget=TextViewWidget(self.textview)
        self.layout_grid.attach(textview_widget,1,row,1,1)
        
        
        