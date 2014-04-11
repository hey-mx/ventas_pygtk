import sys
import pygtk
pygtk.require("2.0")
import gtk
from utils.Form import FormBuilder
from utils.Database import DataModel
from utils.Config import get_pdf_reader, get_margen

class ConfiguracionesFactory(gtk.Frame):
    
    __record_id = 0

    def __init__(self, main):
        super(ConfiguracionesFactory, self).__init__()
        self.main = main
        builder = gtk.Builder()
        builder.add_from_file("config_frame.glade")
        self.content = builder.get_object("vbox_content")
        self.entry = builder.get_object("pdf_entry")
        self.entry_margen_superior = builder.get_object("margen_superior")
        self.entry_margen_izquierdo = builder.get_object("margen_izquierdo")
        builder.connect_signals(self)
        self.content.reparent(self)
        self.content.show()
        self.config_model = DataModel('Configuracion')
        reader = get_pdf_reader()
        self.entry.set_text(reader['valor'])
        self.__record_id = reader['id']
        self.margen_izquierdo =  get_margen('margen_izquierdo')
        self.margen_superior = get_margen('margen_superior')
        if self.margen_superior is not None:
            self.entry_margen_superior = self.margen_superior
        if self.margen_izquierdo is not None:
            self.entry_margen_izquierdo = self.margen_izquierdo

    def on_aceptar_button_clicked(self, widget):
        pdf = self.entry.get_text()
        if self.__record_id == 0:
            self.config_model.create_record({'parametro': 'pdf_reader', 'valor': pdf})
        else:
            self.config_model.update_record({'parametro': 'pdf_reader', 'valor': pdf}, self.__record_id)

        try:
            float(self.entry_margen_superior.get_text())
        except:
            self._show_error_message('El valor para el margen superior debe de ser numerico')
            return
        if self.margen_superior is None:
            self.config_model.create_record({'parametro': 'margen_superior', 
                    'valor': self.entry_margen_superior.get_text()})
        else:
            self.config_model.update_record({'valor': self.entry_margen_superior.get_text()},
                self.margen_superior['id'])
        
        try:
            float(self.entry_margen_izquierdo.get_text())
        except:
            self._show_error_message('El valor para el margen izquierdo debe de ser numerico')
            return

        if self.margen_izquierdo is None:
            self.config_model.create_record({'parametro': 'margen_izquierdo', 
                    'valor': self.entry_margen_izquierdo.get_text()})
        else:
            self.config_model.update_record({'valor': self.entry_margen_izquierdo.get_text()},
                self.margen_izquierdo['id'])

    def on_cerrar_button_clicked(self, widget):
        page = self.parent.get_current_page()
        self.parent.remove_page(page)
        del self.main.pages[page]

    def _show_error_message(self, message):
        dialog = gtk.MessageDialog(self.parent.parent.parent, gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
        dialog.run()
        dialog.destroy()
