'''
Created on 03.05.2015

@author: vvladych
'''

from gi.repository import Gtk


from ui_tools import add_column_to_treeview

class AbstractListMask(Gtk.Box):

    def __init__(self, columnlist):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.store = Gtk.ListStore(str,str,str,str,str)        
        self.tree = Gtk.TreeView(self.store)          
        
        column_counter=0
        for column in columnlist:
            self.tree.append_column(add_column_to_treeview(column["column"], column_counter, column["hide"]))
            column_counter+=1
                    
        self.tree.get_column(0).set_sort_order(Gtk.SortType.ASCENDING)
        self.tree.get_column(0).set_sort_column_id(0)
        
        self.tree.set_size_request(200,300)
        self.pack_start(self.tree, False, False, 0)        

        self.populate_object_view_table()
        
        

    def populate_object_view_table(self):
        raise "populate_object_view_table still unimplemented!"
    

    def delete_object(self):
        raise "delete_object still unimplemented!"
    
    def get_current_object(self):
        raise "get_current_object still unimplemented!"

        