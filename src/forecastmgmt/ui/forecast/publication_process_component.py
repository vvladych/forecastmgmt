'''
Created on 20.05.2015

@author: vvladych
'''
from gi.repository import Gtk

from forecastmgmt.ui.forecast.abstract_data_process_component import AbstractDataOverviewComponent, AbstractDataManipulationComponent, AbstractDataProcessComponent 

from forecastmgmt.ui.ui_tools import TreeviewColumn, show_info_dialog

from forecastmgmt.model.publisher import Publisher


from forecastmgmt.dao.db_connection import get_db_connection
import psycopg2.extras


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
        
        
        self.publication_date_textentry=Gtk.Entry()
        parent_layout_grid.attach(self.publication_date_textentry,1,row,1,1)
        
        publication_date_choose_button=Gtk.Button("Choose date")
        parent_layout_grid.attach(publication_date_choose_button,2,row,1,1)
        publication_date_choose_button.connect("clicked", self.show_calendar)
        

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
        pass
    
    def delete_action(self, widget):
        pass
    
    def show_calendar(self, widget):
        self.calendar_window=Gtk.Dialog()
        self.calendar_window.action_area.hide()
        self.calendar_window.set_decorated(False)
        self.calendar_window.set_property('skip-taskbar-hint', True)
        self.calendar_window.set_size_request(200,200)
                
        self.calendar=Gtk.Calendar()
        self.calendar.connect('day-selected-double-click', self.day_selected, None)
        self.calendar_window.vbox.pack_start(self.calendar, True, True, 0)
        self.calendar.show()
        self.calendar_window.run()
        
        
    def day_selected(self, calendar, event):
        (year,month,day)=self.calendar.get_date()
        self.publication_date_textentry.set_text("%s.%s.%s" % (day,month,year))
        self.calendar_window.destroy()


class PublicationOverviewComponent(AbstractDataOverviewComponent):
    
    treecolumns=[TreeviewColumn("publication_sid", 0, True)]
    
    def __init__(self, forecast):
        self.forecast=forecast
        super(PublicationOverviewComponent, self).__init__(PublicationOverviewComponent.treecolumns)
        

    def create_layout(self, parent_layout_grid, row):
        row += 1
        
        parent_layout_grid.attach(self.treeview,0,row,4,1)
                
        return row

    def populate_model(self):
        self.treemodel.clear()
        pass