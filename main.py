import sys
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
from Proveedores import ProveedoresFactory
from Productos import ProductosFactory
from Ventas import VentasFactory

class MainWindowGtk:
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file("frame.glade")
        self.notebook = builder.get_object('notebook_content')
        builder.connect_signals(self)

    def on_productos_button_clicked(self, widget):
        productos_factory = ProductosFactory()
        self.__add_tab('Productos', productos_factory)

    def on_proveedores_button_clicked(self, widget):
        pro_factory = ProveedoresFactory()
        self.__add_tab('Proveedores', pro_factory)

    def on_ventas_button_clicked(self, widget):
        ventas_factory = VentasFactory()
        self.__add_tab('Ventas', ventas_factory)

    def on_window1_destroy(self, widget):
        gtk.main_quit()

    def __add_tab(self, label, content_object):
        self.notebook.append_page(content_object, gtk.Label(label))
        content_object.show()

if __name__ == "__main__":
    hwg = MainWindowGtk()
    gtk.main()
