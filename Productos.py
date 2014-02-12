import sys
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
from utils.Form import FormBuilder
from utils.Busqueda import BusquedaWindow
from utils.Database import DataModel

class ProductosFactory(gtk.Frame):

    def __init__(self):
        super(ProductosFactory, self).__init__()
        builder = gtk.Builder()
        builder.add_from_file("prod_frame.glade")
        self.content = builder.get_object("vbox_content")
        self.proveedor = builder.get_object("proveedor")
        builder.connect_signals(self)
        self.content.reparent(self)
        self.content.show()
        self.form_builder = FormBuilder(builder, 'Producto')
        self._load_proveedor_combobox()
        
    def _load_proveedor_combobox(self):
        model = DataModel('Proveedor')
        proveedores = model.get_records()
        combo_model = gtk.ListStore(int, str)
        for row in proveedores:
            combo_model.append([int(row['id']), row['nombre']])
        self.proveedor.set_model(combo_model)
        self.proveedor.show()

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

    def _load_entity_from_search(self, value):
        self.form_builder.get_entity(int(value))

    def on_buscar_button_clicked(self, widget):
        busqueda = BusquedaWindow('Producto', self._load_entity_from_search,
            search_fields={'id': 'match', 'nombre': 'like'}, 
            display_fields = ['id', 'nombre', 'precio_compra', 'precio_venta', 'existencia'])
