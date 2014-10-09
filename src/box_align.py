#! /usr/bin/python

__author__="vvladych"
__date__ ="$08.10.2014 04:53:07$"


class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Forecaster")
        self.set_default_size(600,600)
        
        
        

def main():
    print("hell")
    win = MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
