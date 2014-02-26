# -*- coding: utf-8 -*-
import pygtk
pygtk.require("2.0")
import gtk, gobject
from utils.Form import FormBuilder
from utils.Busqueda import BusquedaWindow
from utils.Database import DataModel
from decimal import *
import datetime

class VentasFactory(gtk.Frame):
    
    __id_venta = 0

    def __init__(self, main):
        super(VentasFactory, self).__init__()
        self.main = main
        self.builder = gtk.Builder()
        self.builder.add_from_file("ventas_frame.glade")
        self.builder.connect_signals(self)
        content = self.builder.get_object("vbox_content")
        content.reparent(self)
        content.show()
        self.form_builder = FormBuilder(self.builder, 'Producto')
        self.producto_model = self.form_builder.get_model()
        self.venta_model = DataModel('Venta')
        self.venta_detalle_model = DataModel('VentaDetalle')
        self.ventas_grid = self.builder.get_object('ventas_grid')
        self._load_ventas_grid()
        self.form_builder.load_widget_value('fecha_hora_label', 
            datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        self.idevent = gobject.timeout_add(1000, self._update_fecha_hora)

    def on_buscar_producto_button_clicked(self, widget):
        if self.__id_venta != 0:
            self._show_error_message('Esta visualizando el detalle de una venta realizada, de click en el boton nuevo para realizar una nueva venta')
            return
        busqueda = BusquedaWindow('Producto', self._load_producto,
            search_fields={'id': 'match', 'nombre': 'like'},
            display_fields=['id', 'nombre', 'precio_venta', 'existencia'])

    def on_buscar_button_clicked(self, widget):
        busqueda = BusquedaWindow('Venta', self._load_venta,
            search_fields={'id': 'match', 'fecha_sistema': 'match'},
            display_fields=['id', 'fecha_sistema', 'sub_total', 'impuesto', 'total'])


    def on_agregar_button_clicked(self, widget):
        if self.__id_venta != 0:
            self._show_error_message('Esta visualizando el detalle de una venta realizada, de click en el boton nuevo para realizar una nueva venta')
            return
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
        append = True
        producto = self.producto_model.get_record(int(id_producto))
        if producto:
            if producto['existencia'] < cantidad_producto:
                self._show_error_message('No existe la cantidad necesaria del producto en inventario')
                return
            for row in self.ventas_grid_model:
                if int(row[0]) == id_producto:
                    row[2] = int(row[2]) + cantidad_producto
                    row[4] = str(round(int(row[2]) * Decimal(row[3]), 2))
                    append = False
                    break
            if append:
                self.ventas_grid_model.append([str(id_producto), nombre_producto,
                    str(cantidad_producto), str(round(precio_producto, 2)), 
                        str(round(cantidad_producto * precio_producto, 2))])
            self._clear_producto(True)
            self._ensure_ventas_grid()
            self._calcular_totales()
            gobject.source_remove(self.idevent)
        else:
            self._show_error_message('El codigo de producto no existe')

    def on_eliminar_butto_clicked(self, widget):
        if self.__id_venta != 0:
            self._show_error_message('Esta visualizando el detalle de una venta realizada, de click en el boton nuevo para realizar una nueva venta')
            return
        selection = self.ventas_grid.get_selection()
        model, treeiter = selection.get_selection_selected()
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
        self.__id_venta = 0
        self._clear_producto(True)
        self._clear_venta()
        self.ventas_grid_model.clear()
        self._ensure_ventas_grid()
        self._update_fecha_hora()

    def on_guardar_button_clicked(self, widget):
        total = self.form_builder.get_widget_value('total_label').replace(',', '')
        if self.__id_venta == 0:
            if self._show_save_continue():
                fecha_hora = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                fecha_sistema = datetime.datetime.now().strftime("%Y/%m/%d")
                sub_total = self.form_builder.get_widget_value('subtotal_label').replace(',', '')
                impuesto = self.form_builder.get_widget_value('iva_label').replace(',', '')
                id_venta = self.venta_model.create_record({'fecha_hora': fecha_hora, 'sub_total': sub_total,
                    'impuesto': impuesto, 'total': total, 'fecha_sistema': fecha_sistema})
                if id_venta:
                    for row in self.ventas_grid_model:
                        producto = self.producto_model.get_record(int(row[0]))
                        if producto:
                            self.venta_detalle_model.create_record({'venta_id': str(id_venta), 'producto_id': row[0],
                                'producto_precio': row[3], 'producto_cantidad': row[2],
                                'subtotal': row[4], 'nombre': row[1]})
                            self.producto_model.update_record({'existencia': str(int(producto['existencia']) - int(row[2]))}, 
                                int(row[0]))
                self._clear_producto(True)
                self._clear_venta()
                self.ventas_grid_model.clear()
                self._ensure_ventas_grid()
                self.idevent = gobject.timeout_add(1000, self._update_fecha_hora)
        else:
            self._show_error_message('Esta visualizando el detalle de una venta realizada, de click en el boton nuevo para realizar una nueva venta')

    def on_cancelar_button_clicked(self, widget):
        page = self.parent.get_current_page()
        self.parent.remove_page(page)
        del self.main.pages[page]

    def _calcular_totales(self):
        subtotal = 0.00
        impuesto = 0.00
        total = 0.00
        for row in self.ventas_grid_model:
            precio = Decimal(row[3]) * int(row[2])
            subtotal += round(precio, 2)
        if self.form_builder.get_widget_value('iva_check'):
            impuesto = round(subtotal * 0.16, 2)
            self.form_builder.load_widget_value('iva_label', '{:20,.2f}'.format(impuesto))
        else:
            self.form_builder.load_widget_value('iva_label', '0.00')
        total = round(subtotal + impuesto, 2)
        self.form_builder.load_widget_value('subtotal_label', '{:20,.2f}'.format(subtotal))
        self.form_builder.load_widget_value('total_label', '{:20,.2f}'.format(total))

    def _load_ventas_grid(self):
        self.ventas_grid_model = gtk.ListStore(str, str, str, str, str)
        count = 0
        columns = ['Id Producto', 'Producto', 'Cantidad', 'Precio', 'Subtotal']
        sizes = [50, 200, 60, 100, 100]
        for column in columns:
            render = gtk.CellRendererText()
            column_instance = gtk.TreeViewColumn(column, render, text=count)
            column_instance.set_min_width(sizes[count])
            self.ventas_grid.append_column(column_instance)
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
        self.form_builder.load_widget_value('iva_label', '0.00')

    def _show_error_message(self, message):
        dialog = gtk.MessageDialog(self.parent.parent.parent, gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
        dialog.run()
        dialog.destroy()

    def _show_save_continue(self):
        dialog = gtk.MessageDialog(self.parent.parent.parent, gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, '¿Desea guardad la venta actual?')
        response = dialog.run()
        dialog.destroy()
        return response

    def _update_fecha_hora(self):
        self.form_builder.load_widget_value('fecha_hora_label', 
            datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        self.idevent = gobject.timeout_add(1000, self._update_fecha_hora)

    def _load_venta(self, value):
        venta = self.venta_model.get_record(int(value))
        if venta:
            self.__id_venta = venta['id']
            self.form_builder.load_widget_value('subtotal_label', '{:20,.2f}'.format(float(venta['sub_total'])))
            self.form_builder.load_widget_value('iva_label', '{:20,.2f}'.format(float(venta['impuesto'])))
            self.form_builder.load_widget_value('total_label', '{:20,.2f}'.format(float(venta['total'])))
            gobject.source_remove(self.idevent)
            self.form_builder.load_widget_value('fecha_hora_label', self._parse_fecha(str(venta['fecha_hora'])))
            items = self.venta_detalle_model.get_records(venta_id=venta['id'])
            if len(items) > 0:
                for item in items:
                    self.ventas_grid_model.append([str(item['id']), item['nombre'],
                        str(item['producto_cantidad']), str(round(item['producto_precio'], 2)), 
                            str(round(item['producto_cantidad'] * item['producto_precio'], 2))])
        else:
            self._show_error_message('La venta seleccionada no existe')

    def _parse_fecha(self, fecha):
        year = fecha[:4]
        month = fecha[4:6]
        day = fecha[6:8]
        hour = fecha[8:10]
        minutes = fecha[10:12]
        seconds = fecha[12:14]
        return "%s/%s/%s %s:%s:%s" % (year, month, day, hour, minutes, seconds)
