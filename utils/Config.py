from utils.Database import DataModel

def get_pdf_reader():
    config_model = DataModel('Configuracion')
    pdf = config_model.get_records(parametro = 'pdf_reader')
    if len(pdf) > 0:
        for item in pdf:
            return item

def get_margen(tipo):
    config_model = DataModel('Configuracion')
    margen = config_model.get_records(parametro = tipo)
    if len(margen) > 0:
        for item in margen:
            return item
    return None