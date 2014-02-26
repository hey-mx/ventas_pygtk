import pygtk
pygtk.require('2.0')
import gtk
from utils.Form import FormBuilder
from datetime import datetime
from dateutil.relativedelta import relativedelta

class FiltroFecha:

    def __init__(self, on_aceptar_handler):
        self.on_aceptar_handler = on_aceptar_handler
        builder = gtk.Builder()
        builder.add_from_file('filtro_fecha_frame.glade')
        builder.connect_signals(self)
        self.form_builder = FormBuilder(builder, 'Venta') 
        start_date = datetime.today() - relativedelta(days=15)
        end_date = datetime.today()
        self.form_builder.load_widget_value('fecha_inicio', 
            [start_date.year, start_date.month - 1, start_date.day])
        self.form_builder.load_widget_value('fecha_fin',
            [end_date.year, end_date.month - 1, end_date.day])
        self.window = builder.get_object('fecha_filtro_window')
        self.window.show()

    def on_aceptar_btn_clicked(self, widget):
        self.window.destroy()
        self.on_aceptar_handler(self.form_builder.get_widget_value('fecha_inicio'),
            self.form_builder.get_widget_value('fecha_fin'))
        

    def on_cancelar_btn_clicked(self, widget):
        self.window.destroy()

