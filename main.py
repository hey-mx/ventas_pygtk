# -*- coding: utf-8 -*-
import sys
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
from Proveedores import ProveedoresFactory
from Productos import ProductosFactory
from Ventas import VentasFactory
from ReporteVentas import Ventas
from ReporteProductos import Productos
from Configuraciones import ConfiguracionesFactory

class MainWindowGtk:
    pages = []
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file("frame.glade")
        self.notebook = builder.get_object('notebook_content')
        self.reportes_button = builder.get_object('reportes_button')
        builder.connect_signals(self)
        self.__load_reportes_menu(builder.get_object('reporte_menu'))

    def on_productos_button_clicked(self, widget):
        productos_factory = ProductosFactory(self)
        self.__add_tab('Productos', productos_factory)

    def on_proveedores_button_clicked(self, widget):
        pro_factory = ProveedoresFactory(self)
        self.__add_tab('Proveedores', pro_factory)

    def on_ventas_button_clicked(self, widget):
        ventas_factory = VentasFactory(self)
        self.__add_tab('Ventas', ventas_factory)

    def on_window1_destroy(self, widget):
        gtk.main_quit()

    def on_ventas_reporte_item_activate(self, widget):
        reporte_ventas = Ventas()

    def on_productos_reporte_item_activate(self, widget):
        reporte_productos = Productos()

    def on_productos_agotados_reporte_item_activate(self, widget):
        reporte_productos = Productos(True)

    def on_configuracion_button_clicked(self, widget):
        config_factory = ConfiguracionesFactory(self)
        self.__add_tab('Configuración', config_factory)

    def __add_tab(self, label, content_object):
        if label not in self.pages:
            self.pages.append(label)
            self.notebook.append_page(content_object, gtk.Label(label))
            content_object.show()
        page_number = self.pages.index(label)
        self.notebook.set_current_page(page_number)

    def __load_reportes_menu(self, menu):
        self.reportes_button.set_menu(menu)
        self.reportes_button.show()

if __name__ == "__main__":
    hwg = MainWindowGtk()
    gtk.main()
