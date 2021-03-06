
from gi.repository import Gtk
import time

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
    
    
class DateWidget(Gtk.Grid):
    
    def __init__(self, day_text_entry, month_text_entry, year_text_entry):
        Gtk.Grid.__init__(self)
        self.day_text_entry=day_text_entry
        self.month_text_entry=month_text_entry
        self.year_text_entry=year_text_entry
        self.create_date_grid(True)
        

    def create_date_grid(self, show_calendar=False):
        self.set_column_spacing(5)
        self.day_text_entry.set_max_length(2)
        self.day_text_entry.set_width_chars(2)
        
        self.attach(self.day_text_entry,0,0,1,1)
            
        self.month_text_entry.set_max_length(2)
        self.month_text_entry.set_width_chars(2)
        self.attach_next_to(self.month_text_entry, self.day_text_entry, Gtk.PositionType.RIGHT, 1, 1)
        
        self.year_text_entry.set_max_length(4)
        self.year_text_entry.set_width_chars(4)
        self.attach_next_to(self.year_text_entry, self.month_text_entry, Gtk.PositionType.RIGHT, 1, 1)
        
        self.attach(Gtk.Label("DD"),0,1,1,1)
        self.attach(Gtk.Label("MM"),1,1,1,1)
        self.attach(Gtk.Label("YYYY"),2,1,1,1)
        
        self.set_hexpand(False)
        
        if show_calendar==True:
            pick_date_button=Gtk.Button("Pick date")
            self.attach(pick_date_button,3,0,1,1)
            pick_date_button.connect("clicked", self.show_calendar)
        
    
    def show_calendar(self, widget ):
        self.calendar_window=Gtk.Dialog()
        self.calendar_window.action_area.hide()
        self.calendar_window.set_decorated(False)
        self.calendar_window.set_property('skip-taskbar-hint', True)
        self.calendar_window.set_size_request(200,200)
                
        calendar=Gtk.Calendar()
        calendar.connect('day-selected-double-click', self.day_selected, None)
        self.calendar_window.vbox.pack_start(calendar, True, True, 0)
        calendar.show()
        self.calendar_window.run()
        
        
    def day_selected(self, calendar, event):
        (year,month,day)=calendar.get_date()
        month=month+1
        self.day_text_entry.set_text("%s" % day)
        self.month_text_entry.set_text("%s" % month)
        self.year_text_entry.set_text("%s" % year)
        self.calendar_window.destroy() 
        
        
    def set_date_from_string(self, date_as_string):
        tm=time.strptime(date_as_string, "%Y-%m-%d")
        self.day_text_entry.set_text("%s" % tm.tm_mday)
        self.month_text_entry.set_text("%s" % tm.tm_mon)
        self.year_text_entry.set_text("%s" % tm.tm_year)
        
        
class TextViewWidget(Gtk.Grid):
    
    def __init__(self, textview, model_text=None):
        Gtk.Grid.__init__(self)
        self.textview=textview
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.model_text=model_text
        self.create_textview_widget()
        
    def create_textview_widget(self):
        scrolledwindow= Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        if self.model_text!=None:
            self.textview.get_buffer().set_text(self.model_text)
        scrolledwindow.add(self.textview)
        self.attach(scrolledwindow,0,1,1,1)
        
    def get_textview_text(self):
        textbuffer=self.textview.get_buffer()
        return textbuffer.get_text(textbuffer.get_start_iter(),textbuffer.get_end_iter(),True)
    
    def set_text(self, text):
        if text!=None:
            textbuffer=self.textview.get_buffer()
            textbuffer.set_text("%s" % text)     
        
