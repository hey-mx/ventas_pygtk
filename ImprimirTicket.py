# -*- coding: utf-8 -*-
from utils.Database import DataModel
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from utils.Config import get_pdf_reader, get_margen
from utils.number_to_string import to_word
import subprocess

class Ticket:

    __meses = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo',
        6: 'Junio', 7: 'Julio', 8: 'Agosto', 9: 'Septiembre',
        10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}

    def __init__(self, id_venta):
        self.c = canvas.Canvas('Ticket.pdf')
        self.venta_model = DataModel('Venta')
        self.venta_detalle_model = DataModel('VentaDetalle')
        self.producto_model = DataModel('Producto')
        self.id_venta = id_venta

    def imprimir(self):
        #1 cm = 28.346 puntos
        if self.id_venta > 0:
            x = get_margen('margen_izquierdo')
            print x
            x = 3.92 if x is None else float(x['valor'])

            y = get_margen('margen_superior')
            print y
            y = 692.0 if y is None else float(y['valor'])
            y_inicial = y 
            venta = self.obtener_venta()
            if len(venta) == 0:
                return False
            self.c.setFont("Helvetica", 8)
            self.c.drawString(x + 79.08, y, 
                str(self.fecha_parser(venta['fecha'], 'dia')))
            self.c.drawString(x + 118.08, y, 
                str(self.fecha_parser(venta['fecha'], 'mes')))
            self.c.drawString(x + 264.08, y, 
                str(self.fecha_parser(venta['fecha'], 'anyo')))
            y -= 48.14
            items = self.venta_detalle_model.get_records(venta_id=venta['id'])
            if len(items) > 0:
                for item in items:
                    piezas = ' piezas' if int(item['producto_cantidad']) > 1 else ' pieza'
                    self.c.drawString(x, y, str(item['producto_cantidad']) + piezas)
                    self.c.drawString(x + 49.91, y, item['nombre'][0:30])
                    self.c.drawString(x + 165.70, y, '{:20,.2f}'.format(item['producto_precio']))
                    self.c.drawString(x + 214.70, y, '{:20,.2f}'.format(item['subtotal']))
                    y -= 18.06
            self.c.drawString(x + 208.08, y_inicial - 284.0, 
                '{:20,.2f}'.format(float(venta['total'])))
            self.c.drawString(x + 49.08, y_inicial - 308.0, self.total_a_cadena(venta['total']))
            self.c.showPage()
            self.c.setPageSize((432, 544))
            self.c.save()
            reader = get_pdf_reader()
            if reader and reader['valor'] != '':
                subprocess.Popen([reader['valor'], "Ticket.pdf"])
            return True
        else:
            return False

    def obtener_venta(self):
        venta_info = {}
        venta = self.venta_model.get_record(int(self.id_venta))
        if venta:
            total = float(venta['total'].strip()) if not isinstance(venta['total'], float) else venta['total']
            venta_info = {'id': venta['id'], 'total': total, 'fecha': venta['fecha_sistema']}
        return venta_info

    def fecha_parser(self, fecha, dato):
        if dato is 'dia':
            return int(fecha[8:10])
        if dato is 'mes':
            mes = int(fecha[5:7])
            return self.__meses[mes]
        if dato is 'anyo':
            return fecha[3:4]

    def total_a_cadena(self, total):
        total_neto = int(float(total))
        cadena = to_word(total_neto) + 'Pesos'
        decimales = self.obtener_decimales(total)
        cadena += ' %s/100 M.N' % decimales
        return cadena

    def obtener_decimales(self, total):
        cadena = '{:20,.2f}'.format(total)
        decimales = ''
        agregar = False
        index = 0
        while index < len(cadena):
            if agregar:
                decimales += cadena[index]
            if cadena[index] == '.':
                agregar = True
            index += 1
        if decimales == '':
            decimales = '00'
        return decimales