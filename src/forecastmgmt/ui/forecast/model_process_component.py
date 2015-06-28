'''
Created on 27.05.2015

@author: vvladych
'''
from gi.repository import Gtk

from forecastmgmt.ui.forecast.abstract_data_process_component import AbstractDataOverviewComponent, AbstractDataManipulationComponent, AbstractDataProcessComponent 

from forecastmgmt.ui.ui_tools import TreeviewColumn, show_info_dialog

from forecastmgmt.model.fc_model import FCModel
from model_state_add_dialog import  ModelStateAddDialog


class ModelProcessComponent(AbstractDataProcessComponent):
    
    def __init__(self, forecast):
        super(ModelProcessComponent, self).__init__(ModelManipulationComponent(forecast, ModelOverviewComponent(forecast)))
        

class ModelManipulationComponent(AbstractDataManipulationComponent):
    
    def __init__(self, forecast, overview_component):
        super(ModelManipulationComponent, self).__init__(overview_component)
        self.forecast=forecast
        
    def create_layout(self, parent_layout_grid, row):
        self.parent_layout_grid=parent_layout_grid

        row+=1
        model_uuid_label = Gtk.Label("Model UUID")
        model_uuid_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(model_uuid_label,0,row,1,1)
        
        self.model_uuid_entry=Gtk.Entry()
        self.model_uuid_entry.set_editable(False)
        parent_layout_grid.attach(self.model_uuid_entry,1,row,1,1)
        

        row+=1

        model_short_desc_label = Gtk.Label("Short description")
        model_short_desc_label.set_justify(Gtk.Justification.LEFT)
        parent_layout_grid.attach(model_short_desc_label,0,row,1,1)


        self.model_short_desc_entry=Gtk.Entry()
        parent_layout_grid.attach(self.model_short_desc_entry,1,row,1,1)

        
        row+=2
        
        self.add_state_button=Gtk.Button("Add", Gtk.STOCK_ADD)
        parent_layout_grid.attach(self.add_state_button,0,row,1,1)
        self.add_state_button.connect("clicked", self.add_model_action)
                
        self.delete_button=Gtk.Button("Delete", Gtk.STOCK_DELETE)
        self.delete_button.connect("clicked", self.delete_action)        
        parent_layout_grid.attach(self.delete_button,1,row,1,1)

        row+=3
        
        row=self.overview_component.create_layout(parent_layout_grid, row)
        
        row += 1

        return row
    
        
    
    def add_model_action(self, widget):
        
        fc_model = FCModel(forecast_sid=self.forecast.sid)
        fc_model.insert()
        
        show_info_dialog("Add successful")
        self.overview_component.clean_and_populate_model()
                
        
    def delete_action(self, widget):
        model,tree_iter = self.overview_component.treeview.get_selection().get_selected()
        (model_sid)=model.get(tree_iter, 1)
        FCModel(model_sid).delete()
        model.remove(tree_iter)   
        show_info_dialog("Delete successful")   

    
class ModelOverviewComponent(AbstractDataOverviewComponent):
    
    treecolumns=[TreeviewColumn("forecast_sid", 0, True), TreeviewColumn("model_sid", 1, True), 
                TreeviewColumn("Date", 2, False), TreeviewColumn("Short desc.", 3, False),
                TreeviewColumn("UUID", 4, False)]
    
    def __init__(self, forecast):
        self.forecast=forecast
        super(ModelOverviewComponent, self).__init__(ModelOverviewComponent.treecolumns)
        

    def create_layout(self, parent_layout_grid, row):
        row += 1
        parent_layout_grid.attach(self.treeview,0,row,4,1)
        return row

        
    def populate_model(self):
        self.treemodel.clear()
        for model in FCModel().get_all_for_foreign_key(self.forecast.sid):     
            self.treemodel.append(["%s" % model.forecast_sid, "%s" % model.sid, model.model_date, None, model.uuid])
            

    def on_row_select(self,widget,path,data):
        dialog=ModelStateAddDialog(self, self.get_active_model())
        dialog.run()
        dialog.destroy()
        
        
    def get_active_model(self):
        model,tree_iter=self.treeview.get_selection().get_selected()
        model_sid=model.get(tree_iter, 1)
        return model_sid
    
