'''
Created on 14.03.2015

@author: vvladych
'''

from gi.repository import Gtk


from ui_tools import add_column_to_treeview


class ProjectOverviewWindow(Gtk.Grid):
    
    def __init__(self, main_window, forecast=None):
        Gtk.Grid.__init__(self)
        self.main_window=main_window
        self.create_layout()
        self.forecast=forecast
        self.load_forecast()
        
        
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
        # project originators
        originators_label = Gtk.Label("Originators")
        originators_label.set_justify(Gtk.Justification.LEFT)
        self.attach(originators_label,0,row,2,1)
        
        row += 1
        self.__add_forecast_originators_treeview()
        self.attach(self.originators_treeview,0,row,2,1)
        
        row += 1
        self.add_originator_button=Gtk.Button("Add", Gtk.STOCK_ADD)
        self.attach(self.add_originator_button,0,row,1,1)
        self.remove_originator_button=Gtk.Button("Delete", Gtk.STOCK_DELETE)
        self.attach(self.remove_originator_button,1,row,1,1)

        
        row += 1
        # project publications
        publications_label = Gtk.Label("Publications")
        publications_label.set_justify(Gtk.Justification.LEFT)
        self.attach(publications_label,0,row,2,1)
        
        row += 1
        self.__add_forecast_publications_treeview()
        self.attach(self.publications_treeview,0,row,2,1)
        
        row += 1
        self.add_publication_button=Gtk.Button("Add", Gtk.STOCK_ADD)
        self.attach(self.add_publication_button,0,row,1,1)
        self.remove_publication_button=Gtk.Button("Delete", Gtk.STOCK_DELETE)
        self.attach(self.remove_publication_button,1,row,1,1)
        
        row += 1
        # project model
        model_label = Gtk.Label("Model")
        model_label.set_justify(Gtk.Justification.LEFT)
        self.attach(model_label,0,row,2,1)
        
        
    def load_forecast(self):
        if self.forecast!=None:
            self.forecast_uuid_text_entry.set_text(self.forecast.forecast_uuid)
            
    def __add_forecast_publications_treeview(self):
        self.publications_treestore = Gtk.TreeStore(str,str,str)
        self.publications_treeview = Gtk.TreeView(self.publications_treestore)
        self.publications_treeview.append_column(add_column_to_treeview("id", 0, True))
        self.publications_treeview.append_column(add_column_to_treeview("Role", 1, False))
        self.publications_treeview.append_column(add_column_to_treeview("Value", 2, False))
        self.publications_treeview.set_size_request(200,100)
        #self.publications_treeview.connect("row-activated", self.on_row_selection)
        

    def __add_forecast_originators_treeview(self):
        self.originators_treestore = Gtk.TreeStore(str,str,str)
        self.originators_treeview = Gtk.TreeView(self.originators_treestore)
        self.originators_treeview.append_column(add_column_to_treeview("id", 0, True))
        self.originators_treeview.append_column(add_column_to_treeview("Role", 1, False))
        self.originators_treeview.append_column(add_column_to_treeview("Value", 2, False))
        self.originators_treeview.set_size_request(200,100)

        