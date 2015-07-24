'''
Created on 27.05.2015

@author: vvladych
'''
from gi.repository import Gtk

from forecastmgmt.ui.forecast.abstract_data_process_component import AbstractDataOverviewComponent, AbstractDataManipulationComponent, AbstractDataProcessComponent 

from forecastmgmt.ui.ui_tools import TreeviewColumn, show_info_dialog

from forecastmgmt.model.model_text import ModelText

from forecastmgmt.dao.db_connection import get_db_connection
import psycopg2.extras

class TextModelProcessComponent(AbstractDataProcessComponent):
    
    def __init__(self, forecast):
        super(TextModelProcessComponent, self).__init__(TextModelManipulationComponent(forecast, TextModelOverviewComponent(forecast)))
        

class TextModelManipulationComponent(AbstractDataManipulationComponent):
    
    def __init__(self, forecast, overview_component):
        super(TextModelManipulationComponent, self).__init__(overview_component)
        self.forecast=forecast
        
    def create_layout(self, parent_layout_grid, row):
        row+=1
        # Add model text view
        scrolledwindow= Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.forecast_model_textview=Gtk.TextView()
        if self.forecast.model_text!=None:
            self.forecast_model_textview.get_buffer().set_text(self.forecast.model_text.model_text)
        scrolledwindow.add(self.forecast_model_textview)
        parent_layout_grid.attach(scrolledwindow,0,row,1,1)
                
        row+=1
        # Add save button
        self.save_model_button=Gtk.Button("Save", Gtk.STOCK_SAVE)
        parent_layout_grid.attach(self.save_model_button,1,row,1,1)
        self.save_model_button.connect("clicked", self.save_model_action)

        
    def save_model_action(self, widget):
        textbuffer=self.forecast_model_textview.get_buffer()
        model_text=textbuffer.get_text(textbuffer.get_start_iter(),textbuffer.get_end_iter(),True)
        if self.forecast.model_text==None:
            show_info_dialog("insert text")
            ModelText(forecast_sid=self.forecast.sid, model_text=model_text).insert()
            self.forecast.load_model_text()
        else:
            if self.forecast.model_text.model_text!=model_text:
                self.forecast.model_text.update(model_text=model_text)
                show_info_dialog("update model text")
                self.forecast.load_model_text()
                self.forecast_model_textview.get_buffer().set_text(self.forecast.model_text.model_text)
            else:
                show_info_dialog("nothing to update")

    
class TextModelOverviewComponent(AbstractDataOverviewComponent):
    
    treecolumns=[TreeviewColumn("model_text_sid", 0, True), TreeviewColumn("model text", 1, False)]

    
    def __init__(self, forecast):
        self.forecast=forecast
        super(TextModelOverviewComponent, self).__init__(TextModelOverviewComponent.treecolumns)
        

    def populate_model(self):
        self.treemodel.clear()
        cur=get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        data=(self.forecast.sid,)
        cur.execute("""SELECT
                        sid, substring(model_text from 1 for 100) as model_text 
                        FROM 
                        fc_model_text
                        WHERE
                        forecast_sid=%s
                        """,data)
        for p in cur.fetchall():
            self.treemodel.append([ "%s" % p.sid, "%s" % p.model_text])
        cur.close()
