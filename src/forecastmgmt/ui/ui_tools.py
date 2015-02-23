
from gi.repository import Gtk

def add_column_to_treeview(columnname,counter,hidden):
    column=Gtk.TreeViewColumn(columnname)
    if hidden==True:
        column.set_visible(False)
    renderer=Gtk.CellRendererText()
    column.pack_start(renderer,True)
    column.add_attribute(renderer, "text", counter)
    return column