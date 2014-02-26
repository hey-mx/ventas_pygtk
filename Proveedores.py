import sys
import pygtk
pygtk.require("2.0")
import gtk
from utils.Form import FormBuilder
from utils.Busqueda import BusquedaWindow

class ProveedoresFactory(gtk.Frame):

    def __init__(self, main):
        super(ProveedoresFactory, self).__init__()
        self.main = main
        builder = gtk.Builder()
        builder.add_from_file("pro_frame.glade")
        self.content = builder.get_object("vbox_content")
        builder.connect_signals(self)
        self.content.reparent(self)
        self.content.show()
        self.form_builder = FormBuilder(builder, 'Proveedor')

    def get_content(self):
        return self.content

    def on_nuevo_button_clicked(self, widget):
        self.form_builder.clear_form()

    def on_guardar_button_clicked(self, widget):
        self.form_builder.save_entity()

    def on_eliminar_button_clicked(self, widget):
        self.form_builder.delete_entity()

    def on_cancelar_button_clicked(self, widget):
        page = self.parent.get_current_page()
        self.parent.remove_page(page)
        del self.main.pages[page]

    def _load_entity_from_search(self, value):
        self.form_builder.get_entity(int(value))

    def on_buscar_button_clicked(self, widget):
        busqueda = BusquedaWindow('Proveedor', self._load_entity_from_search,
            search_fields={'id': 'match', 'nombre': 'like'})
