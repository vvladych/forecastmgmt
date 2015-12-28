'''
Created on 04.05.2015

@author: vvladych
'''
from gi.repository import Gtk
from src.forecastmgmt.ui.masterdata.masterdata_abstract_window import AbstractListMask
from src.forecastmgmt.model.publisher import Publisher

class PublisherListMask(AbstractListMask):

    treeview_columns=[
                      {"column":"common_name","hide":False},
                      {"column":"URL","hide":False},
                      {"column":"publisher uuid","hide":False},
                      {"column":"publisher_sid","hide":True}
                      
                      ]

    def __init__(self):
        super(PublisherListMask, self).__init__(PublisherListMask.treeview_columns)        
        

    def populate_object_view_table(self):
        self.store.clear()        
        publishers = Publisher().get_all()
        for publisher in publishers:
            self.store.append(["%s" % publisher.common_name, "%s" % publisher.url, "%s" % publisher.uuid, "%s" % publisher.sid])
        

    def delete_object(self):
        model,tree_iter = self.tree.get_selection().get_selected()
        (publisher_sid)=model.get(tree_iter, 3)
        Publisher(publisher_sid).delete()
        self.store.remove(tree_iter)


    def get_current_object(self):
        model,tree_iter = self.tree.get_selection().get_selected()
        (publisher_sid)=model.get(tree_iter, 3)
        return Publisher(publisher_sid)
