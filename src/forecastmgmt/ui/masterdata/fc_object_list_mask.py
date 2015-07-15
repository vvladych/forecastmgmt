'''
Created on 04.05.2015

@author: vvladych
'''
from gi.repository import Gtk
from masterdata_abstract_window import AbstractListMask
from forecastmgmt.model.fc_object import FCObject

class FCObjectListMask(AbstractListMask):

    treeview_columns=[{"column":"common_name","hide":False},{"column":"uuid","hide":False},{"column":"fc_object_sid","hide":True}]

    def __init__(self):
        super(FCObjectListMask, self).__init__(FCObjectListMask.treeview_columns)
        

    def populate_object_view_table(self):
        self.store.clear()        
        fc_objects = FCObject().get_all()
        for fc_object in fc_objects:
            self.store.append(["%s" % fc_object.common_name, "%s" % fc_object.uuid, "%s" % fc_object.sid])
        

    def delete_object(self):
        model,tree_iter = self.tree.get_selection().get_selected()
        (fc_object_sid)=model.get(tree_iter, 2)
        FCObject(fc_object_sid).delete()
        self.store.remove(tree_iter)


    def get_current_object(self):
        model,tree_iter = self.tree.get_selection().get_selected()
        if tree_iter!=None:
            (fc_object_sid)=model.get(tree_iter, 2)
            return FCObject(fc_object_sid)
        else:
            print("Nothing selected!")
