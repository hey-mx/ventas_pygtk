from utils.Database import DataModel
model = DataModel('Proveedor')
#model.get_record(1)
model.update_record({'cp': 72420, 'email_contacto': 'isc.jcjl@gmail.com'}, 1)
model.dispose()
