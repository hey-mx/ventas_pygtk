import sys
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
from utils.Form import FormBuilder
from utils.Database import DataModel
from utils.Config import get_pdf_reader

class ConfiguracionesFactory(gtk.Frame):
    
    __record_id = 0

    def __init__(self, main):
        super(ConfiguracionesFactory, self).__init__()
        self.main = main
        builder = gtk.Builder()
        builder.add_from_file("config_frame.glade")
        self.content = builder.get_object("vbox_content")
        self.entry = builder.get_object("pdf_entry")
        builder.connect_signals(self)
        self.content.reparent(self)
        self.content.show()
        self.config_model = DataModel('Configuracion')
        reader = get_pdf_reader()
        self.entry.set_text(reader['valor'])
        self.__record_id = reader['id']
    

    def on_aceptar_button_clicked(self, widget):
        pdf = self.entry.get_text()
        if self.__record_id == 0:
            self.config_model.create_record({'parametro': 'pdf_reader', 'valor': pdf})
        else:
            self.config_model.update_record({'parametro': 'pdf_reader', 'valor': pdf}, self.__record_id)

    def on_cerrar_button_clicked(self, widget):
        page = self.parent.get_current_page()
        self.parent.remove_page(page)
        del self.main.pages[page]
