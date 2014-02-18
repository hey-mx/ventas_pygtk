import pygtk
pygtk.require("2.0")
import gtk

class ProgressDialog(gtk.Window):

    __progressbar = None

    def __init__(self):
        gtk.Window.__init__(self, type=gtk.WINDOW_TOPLEVEL)
        self.set_title('Progreso')
        self.set_resizable(True)
        self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.set_default_size(300, 30)
        self.set_modal(True)
        self.__progressbar = gtk.ProgressBar()
        self.add(self.__progressbar)
        self.__progressbar.show()

    def set_progress_fraction(self, fraction):
        self.__progressbar.set_fraction(fraction)
