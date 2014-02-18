# -*- coding: utf-8 -*-
import pygtk
pygtk.require("2.0")
import gtk
from utils.Database import DataModel

class FormBuilder:
    __fields = []
    def __init__(self, builder, entity):
        self.builder = builder
        self.entity = entity
        self.model = DataModel(entity)
        self.__fields = self.model.get_colums()

    def get_entity(self, entity_id):
        row = self.model.get_record(entity_id)
        if row is not None:
            for field in self.__fields:
                self.load_widget_value(field, row[field])
    
    def save_entity(self, upsert=False, custom_id=False):
        id = self.__get_id()
        values = {}
        for field in self.__fields:
            if field != 'id' or custom_id == True:
                values[field] = self.get_widget_value(field)
        if id == 0:
            self.model.create_record(values)
        else:
            self.model.update_record(values, id, upsert)
        self.clear_form()

    def delete_entity(self):
        id = self.__get_id()
        if id > 0:
            dialog = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, "¿Desea eliminar el registro actual?")
            response = dialog.run()
            dialog.destroy()
            if response == gtk.RESPONSE_YES:
                self.model.delete_record(id)
                self.clear_form()

    def clear_form(self):
        for field in self.__fields:
            self.load_widget_value(field, '')

    def load_widget_value(self, widget_name, value):
        widget = self.builder.get_object(widget_name)
        if isinstance(widget, gtk.Entry) or isinstance(widget, gtk.Label):
            widget.set_text(str(value))
        if isinstance(widget, gtk.ComboBox):
            model = widget.get_model()
            count = 0
            for row in model:
                if row[0] == value:
                    widget.set_active(count)
                count += 1
        if isinstance(widget, gtk.CheckButton):
            widget.set_active(True if value else False)
        if isinstance(widget, gtk.Calendar):
            widget.select_month(value[1], value[0])
            widget.select_day(value[2])
            
    def get_widget_value(self, widget_name):
        value = None
        widget = self.builder.get_object(widget_name)
        if isinstance(widget, gtk.Entry) or isinstance(widget, gtk.Label):
            value = widget.get_text()
        if isinstance(widget, gtk.ComboBox):
            model = widget.get_model()
            tree_iter = widget.get_active_iter()
            if tree_iter != None:
                value = str(model[tree_iter][0])
        if isinstance(widget, gtk.CheckButton):
            value = widget.get_active()
        if isinstance(widget, gtk.Calendar):
            value = widget.get_date()
        return value

    def get_model(self):
        return self.model

    def __get_id(self):
        id = 0
        widget = self.builder.get_object('id')
        if isinstance(widget, gtk.Label) or isinstance(widget, gtk.Entry):
            try:
                id = int(widget.get_text())
            except:
                pass
        return id
