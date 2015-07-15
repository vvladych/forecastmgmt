
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
    

def add_date_grid(day_text_entry, month_text_entry, year_text_entry):
    birthdate_grid=Gtk.Grid()
    birthdate_grid.set_column_spacing(5)
    day_text_entry.set_max_length(2)
    day_text_entry.set_width_chars(2)
    
    birthdate_grid.attach(day_text_entry,0,0,1,1)
        
    month_text_entry.set_max_length(2)
    month_text_entry.set_width_chars(2)
    birthdate_grid.attach_next_to(month_text_entry, day_text_entry, Gtk.PositionType.RIGHT, 1, 1)
    
    year_text_entry.set_max_length(4)
    year_text_entry.set_width_chars(4)
    birthdate_grid.attach_next_to(year_text_entry, month_text_entry, Gtk.PositionType.RIGHT, 1, 1)
    
    birthdate_grid.attach(Gtk.Label("DD"),0,1,1,1)
    birthdate_grid.attach(Gtk.Label("MM"),1,1,1,1)
    birthdate_grid.attach(Gtk.Label("YYYY"),2,1,1,1)
    
    birthdate_grid.set_hexpand(False)
    return birthdate_grid
