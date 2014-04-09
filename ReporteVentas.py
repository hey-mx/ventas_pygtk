from utils.FiltroFecha import FiltroFecha
from utils.Database import DataModel
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from decimal import *
from subprocess import call
import subprocess
from utils.Config import get_pdf_reader

class Ventas:

    def __init__(self):
        filtro = FiltroFecha(self._run_reporte)


    def _run_reporte(self, fecha_inicio, fecha_fin):
        model_venta = DataModel('Venta')
        model_venta_detalle = DataModel('VentaDetalle')
        model_producto = DataModel('Producto')
        fecha_inicio = datetime.datetime(fecha_inicio[0], fecha_inicio[1] + 1,
            fecha_inicio[2])
        fecha_fin = datetime.datetime(fecha_fin[0], fecha_fin[1] + 1,
            fecha_fin[2])
        fecha_inicio_param = fecha_inicio.strftime("%Y%m%d000000")
        fecha_fin_param = fecha_fin.strftime("%Y%m%d235959")
        query = 'SELECT id, fecha_sistema, sub_total, impuesto, total FROM Venta ' +\
            'WHERE fecha_hora >= ? AND fecha_hora <= ?'
        ventas = model_venta.get_records_from_query(query, [fecha_inicio_param, 
            fecha_fin_param])
        c = canvas.Canvas('ReporteVentas.pdf', pagesize=letter)
        if len(ventas) > 0:
            self.__add_page_header(c, fecha_inicio, fecha_fin)
            c.drawString(60, 680, 'Id Venta')
            c.drawString(140, 680, 'Fecha')
            c.drawString(260, 680, 'Sub Total')
            c.drawString(390, 680, 'IVA')
            c.drawString(490, 680, 'Total')
            y = 650
            total = 0.00
            for venta in ventas:
                total_string = str(venta['total'])
                c.drawString(73, y, str(venta['id']))
                c.drawString(130, y, venta['fecha_sistema'])
                c.drawRightString(310, y, '{:20,.2f}'.format(float(venta['sub_total'])))
                c.drawRightString(420, y, '{:20,.2f}'.format(float(venta['impuesto'])))
                c.drawRightString(520, y, '{:20,.2f}'.format(float(total_string)))
                total += float(total_string)
                items = model_venta_detalle.get_records(venta_id=venta['id'])
                y -= 30
                if len(items) > 0:
                    
                    c.drawString(133, y, 'Producto')
                    c.drawString(253, y, 'Precio')
                    c.drawString(313, y, 'Cantidad')
                    c.drawString(413, y, 'Subtotal')
                    total_registros = len(items)
                    actual = 0
                    for item in items:
                        y -= 20
                        nombre = item['nombre'] if len(item['nombre']) <= 20 else item['nombre'][:19]
                        c.drawRightString(213, y, nombre)
                        c.drawRightString(280, y, '{:20,.2f}'.format(float(item['producto_precio'])))
                        c.drawRightString(353, y, str(item['producto_cantidad']))
                        c.drawRightString(453, y, '{:20,.2f}'.format(float(item['subtotal'])))
                    y -= 20
                    c.line(10, y, 600, y)
                    y -= 20
                    actual += 1
                if y <= 120:
                    self.__add_page_footer(c)
                    y = 680
                    c.showPage()
                    self.__add_page_header(c, fecha_inicio, fecha_fin)
            c.drawString(360, y - 20, 'T O T A L:')
            c.drawRightString(520, y - 20, '{:20,.2f}'.format(total))
            self.__add_page_footer(c)
            c.showPage()
            c.save()
            reader = get_pdf_reader()
            if reader and reader['valor'] != '':
                subprocess.Popen([reader['valor'], "ReporteVentas.pdf"])
    
    def __add_page_header(self, canvas, fecha_inicio, fecha_fin):
        canvas.drawCentredString(300, 750, 'R E P O R T E   D E   V E N T A S')
        canvas.drawCentredString(300, 720, 'DEL: ' +\
            fecha_inicio.strftime('%Y/%m/%d') + ' AL ' + fecha_fin.strftime('%Y/%m/%d'))

    def __add_page_footer(self, canvas):
        canvas.drawRightString(550, 40, str(canvas.getPageNumber()))
