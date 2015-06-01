'''
Created on 04.05.2015

@author: vvladych
'''
from gi.repository import Gtk
from masterdata_abstract_list_mask import AbstractListMask
from forecastmgmt.model.publisher import Publisher

class PublisherListMask(AbstractListMask):

    treeview_columns=[{"column":"common_name","hide":False},{"column":"publisher uuid","hide":False},{"column":"publisher_sid","hide":True}]

    def __init__(self):
        super(PublisherListMask, self).__init__(PublisherListMask.treeview_columns)        
        

    def populate_object_view_table(self):
        self.store.clear()        
        publishers = Publisher().get_all()
        for publisher in publishers:
            self.store.append(["%s" % publisher.common_name, "%s" % publisher.uuid, "%s" % publisher.sid, "", ""])
        

    def delete_object(self):
        model,tree_iter = self.tree.get_selection().get_selected()
        (publisher_sid)=self.store.get(tree_iter, 2)
        Publisher(publisher_sid).delete()
        self.store.remove(tree_iter)


    def get_current_object(self):
        model,tree_iter = self.tree.get_selection().get_selected()
        (publisher_sid)=self.store.get(tree_iter, 2)
        return Publisher(publisher_sid)