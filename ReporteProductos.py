from utils.Database import DataModel
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from utils.Config import get_pdf_reader
import subprocess

class Productos:

    def __init__(self, agotados=False):
        self.__agotados = agotados
        self.__run_reporte()

    def __run_reporte(self):
        model_producto = DataModel('Producto')
        model_proveedor = DataModel('Proveedor')
        if self.__agotados:
            productos = model_producto.get_records_from_query('SELECT * FROM Producto WHERE existencia <= 0 ORDER BY nombre ASC')
        else:
            productos = model_producto.get_records(order='nombre ASC')
        c = canvas.Canvas('ReporteProductos.pdf', pagesize=landscape(letter))
        self.__add_page_header(c)
        total = 0
        if len(productos) > 0:
            y = 490
            for producto in productos:
                c.drawString(30, y, str(producto['id']))
                c.drawRightString(260, y, producto['nombre'])
                proveedor = model_proveedor.get_record(producto['proveedor'])
                if proveedor:
                    c.drawRightString(460, y, proveedor['nombre'])
                c.drawRightString(550, y, '{:20,.2f}'.format(producto['precio_compra']))
                c.drawRightString(660, y, '{:20,.2f}'.format(producto['precio_venta']))
                c.drawRightString(760, y, str(producto['existencia']))
                y -= 20
                if y <= 80:
                    self.__add_page_footer(c)
                    y = 490
                    c.showPage()
                    self.__add_page_header(c)
                total += 1
        c.drawRightString(650, 60, 'T O T A L   D E   P R O D U C T O S:   ' + str(total))
        self.__add_page_footer(c)
        c.showPage()
        c.save()
        reader = get_pdf_reader()
        if reader:
            subprocess.Popen([reader['valor'], "ReporteProductos.pdf"])


    def __add_page_header(self, canvas):
        titulo = 'R E P O R T E   D E   P R O D U C T O S' +\
            ('   A G O T A D O S' if self.__agotados else '')
        y = 520
        canvas.drawCentredString(400, 570, titulo)
        canvas.drawCentredString(400, 540, 'AL: ' +\
            datetime.datetime.today().strftime('%Y/%m/%d %H:%M:%S'))
        canvas.drawString(70, y, 'Id')
        canvas.drawString(180, y, 'Nombre')
        canvas.drawString(320, y, 'Proveedor')
        canvas.drawString(490, y, 'P. Compra')
        canvas.drawString(610, y, 'P. Venta')
        canvas.drawString(710, y, 'Existencia')

    def __add_page_footer(self, canvas):
        canvas.drawRightString(760, 40, str(canvas.getPageNumber()))
