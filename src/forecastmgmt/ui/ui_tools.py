
from gi.repository import Gtk

class TreeviewColumn(object):
    
    def __init__(self, column_name, ordernum, hidden=True, fixed_size=False):
        self.column_name=column_name
        self.ordernum=ordernum
        self.hidden=hidden
        self.fixed_size=fixed_size


def add_column_to_treeview(columnname,counter,hidden,fixed_size=False):
    column=Gtk.TreeViewColumn(columnname)
    if hidden==True:
        column.set_visible(False)
    renderer=Gtk.CellRendererText()
    column.pack_start(renderer,True)
    column.add_attribute(renderer, "text", counter)
    if fixed_size==True:
        column.set_fixed_width(50)
    return column

def show_info_dialog(message):
    info_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, message)
    info_dialog.run()
    info_dialog.destroy()