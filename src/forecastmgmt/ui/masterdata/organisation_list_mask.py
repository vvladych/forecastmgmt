'''
Created on 02.05.2015

@author: vvladych
'''
from gi.repository import Gtk
from masterdata_abstract_window import AbstractListMask
from forecastmgmt.model.organisation import Organisation

class OrganisationListMask(AbstractListMask):

    treeview_columns=[{"column":"common_name","hide":False},{"column":"organisation uuid","hide":False},{"column":"organisation_sid","hide":True}]

    def __init__(self):
        super(OrganisationListMask, self).__init__(OrganisationListMask.treeview_columns)        
        

    def populate_object_view_table(self):
        self.store.clear()        
        organisations = Organisation().get_all()
        for organisation in organisations:
            self.store.append(["%s" % organisation.common_name, "%s" % organisation.uuid, "%s" % organisation.sid, "", ""])
        

    def delete_object(self):
        model,tree_iter = self.tree.get_selection().get_selected()
        (organisation_sid)=self.store.get(tree_iter, 2)
        Organisation(organisation_sid).delete()
        self.store.remove(tree_iter)


    def get_current_object(self):
        model,tree_iter = self.tree.get_selection().get_selected()
        (organisation_sid)=model.get(tree_iter, 2)
        return Organisation(organisation_sid)

