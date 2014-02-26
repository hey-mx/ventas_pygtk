from distutils.core import setup
import py2exe
import os
import sys
import gtk

def generate_data_files(prefix, tree, file_filter=None):
    data_files = []
    for root, dirs, files in os.walk(os.path.join(prefix, tree)):        
        to_dir = os.path.relpath(root, prefix)

        if file_filter is not None:
            file_iter = (fl for fl in files if file_filter(root, fl))
        else:
            file_iter = files

        data_files.append((to_dir, [os.path.join(root, fl) for fl in file_iter]))

    non_empties = [[to, fro] for [to, fro] in data_files if fro]
    return non_empties

# Find GTK+ installation path
__import__('gtk')
m = sys.modules['gtk']
gtk_base_path = m.__path__[0]
GTK_RUNTIME_DIR = os.path.join(
    os.path.split(os.path.dirname(gtk.__file__))[0], "runtime")
GTK_ICONS = os.path.join("share", "icons")

packages= [
    'reportlab',
    'reportlab.lib',
    'reportlab.pdfbase',
    'reportlab.pdfgen',
    'reportlab.platypus',
	'encodings',
]

setup(
    name = 'cdp_app',
    description = 'Control de Productos',
    version = '1.0',

    windows = [
                  {
                      'script': 'puntoventa.py',
                      'icon_resources': [(1, "System-Calc-icon.ico")],
                  }
              ],
    options = {
                  'py2exe': {
                      'packages': packages,
                      'includes': 'gtk, cairo, pango, pangocairo, atk, gobject, gio, gtk.keysyms, sqlite3, dateutil, reportlab',
                  }
              },
    data_files=[
                   'System-Calc-icon.ico',
                   'busqueda.glade',
                   'config_frame.glade',
                   'filtro_fecha_frame.glade',
                   'frame.glade',
                   'prod_frame.glade',
                   'pro_frame.glade',
                   'ventas_frame.glade',
                   'pv.db',
                   #('logos', ['E:\\appGtk\\logos\\120x146.png',
                   #'E:\\appGtk\\logos\\blank.png',
                   #'E:\\appGtk\\logos\\icon.png',
                   #'E:\\appGtk\\logos\\success.png'])
               ]
)
