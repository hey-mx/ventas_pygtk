# -*- coding: utf-8 -*-
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
from utils.Form import FormBuilder
from utils.Busqueda import BusquedaWindow
from utils.Database import DataModel
from decimal import *

class VentasFactory(gtk.Frame):
    
    __id_venta = 0

    def __init__(self):
        super(VentasFactory, self).__init__()
        self.builder = gtk.Builder()
        self.builder.add_from_file("ventas_frame.glade")
        self.builder.connect_signals(self)
        content = self.builder.get_object("vbox_content")
        content.reparent(self)
        content.show()
        self.form_builder = FormBuilder(self.builder, 'Producto')
        self.producto_model = self.form_builder.get_model()
        self.ventas_grid = self.builder.get_object('ventas_grid')
        self._load_ventas_grid()

    def on_buscar_producto_button_clicked(self, widget):
        busqueda = BusquedaWindow('Producto', self._load_producto,
            search_fields={'id': 'match', 'nombre': 'like'},
            display_fields=['id', 'nombre', 'precio_venta', 'existencia'])

    def on_agregar_button_clicked(self, widget):
        id_producto = self.form_builder.get_widget_value('id_producto')
        try:
            id_producto = int(id_producto)
        except:
            self._show_error_message('Escriba un código de producto valido')
            return
        nombre_producto = self.form_builder.get_widget_value('nombre_producto')
        if nombre_producto.strip() == '':
            self._show_error_message('Escriba una descripción del producto')
            return
        precio_producto = self.form_builder.get_widget_value('precio_producto')
        try:
            precio_producto = Decimal(precio_producto)
            if precio_producto < 0:
                raise NameError('Precio no valido')
        except:
            self._show_error_message('Escriba un precio valido')
            return
        cantidad_producto = self.form_builder.get_widget_value('cantidad_producto')
        try:
            cantidad_producto = int(cantidad_producto)
            if cantidad_producto == 0:
                raise NameError('Cantidad no valida')
        except:
            self._show_error_message('Escriba una cantidad valida')
            return
        self.ventas_grid_model.append([str(id_producto), nombre_producto,
            str(cantidad_producto), str(round(precio_producto, 2))])
        self._clear_producto(True)
        self._ensure_ventas_grid()
        self._calcular_totales()

    def on_eliminar_butto_clicked(self, widget):
        selection = self.ventas_grid.get_selection()
        model, treeiter = selection.get_selected()
        if treeiter:
            del model[treeiter]
            self._ensure_ventas_grid()
            self._calcular_totales()

    def on_iva_check_toggled(self, widget):
        self._calcular_totales()

    def _load_producto(self, value):
        self.form_builder.load_widget_value('id_producto', value)

    def on_id_producto_changed(self, widget):
        producto_id = 0
        try:
            producto_id = int(widget.get_text())
        except:
            pass
        producto = self.producto_model.get_record(int(producto_id))
        self._clear_producto()
        if producto:
            self._load_producto_information(producto)

    def on_nuevo_button_clicked(self, widget):
        self._clear_producto(True)
        self._clear_venta()
        self.ventas_grid_model.clear()
        self._ensure_ventas_grid()

    def on_guardar_button_clicked(self, widget):
        self._clear_producto(True)
        self._clear_venta()
        self.ventas_grid_model.clear()
        self._ensure_ventas_grid()

    def on_cancelar_button_clicked(self, widget):
        page = self.parent.get_current_page()
        self.parent.remove_page(page)

    def _calcular_totales(self):
        subtotal = 0.00
        impuesto = 0.00
        total = 0.00
        for row in self.ventas_grid_model:
            precio = Decimal(row[3]) * int(row[2])
            subtotal += round(precio, 2)
        if self.form_builder.get_widget_value('iva_check'):
            impuesto = round(subtotal * 0.16, 2)
        total = round(subtotal + impuesto, 2)
        self.form_builder.load_widget_value('subtotal_label', '{:20,.2f}'.format(subtotal))
        self.form_builder.load_widget_value('total_label', '{:20,.2f}'.format(total))

    def _load_ventas_grid(self):
        self.ventas_grid_model = gtk.ListStore(str, str, str, str)
        count = 0
        for column in ['Id Producto', 'Producto', 'Cantidad', 'Precio']:
            render = gtk.CellRendererText()
            self.ventas_grid.append_column(gtk.TreeViewColumn(column,
                render, text=count))
            count += 1
        self._ensure_ventas_grid()

    def _ensure_ventas_grid(self):
        self.ventas_grid.set_model(self.ventas_grid_model)
        self.ventas_grid.show()

    def _load_producto_information(self, row):
        self.form_builder.load_widget_value('nombre_producto', row['nombre'])
        self.form_builder.load_widget_value('precio_producto', row['precio_venta'])
        self.form_builder.load_widget_value('cantidad_producto', '0')
        self.builder.get_object('cantidad_producto').grab_focus()

    def _clear_producto(self, clear_id=False):
        if clear_id:
            self.form_builder.load_widget_value('id_producto', '')
        self.form_builder.load_widget_value('nombre_producto', '')
        self.form_builder.load_widget_value('precio_producto', '0.00')
        self.form_builder.load_widget_value('cantidad_producto', '0')

    def _clear_venta(self):
        self.form_builder.load_widget_value('subtotal_label', '0.00')
        self.form_builder.load_widget_value('total_label', '0.00')

    def _show_error_message(self, message):
        dialog = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
        dialog.run()
        dialog.destroy()
