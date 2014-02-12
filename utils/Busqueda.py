# -*- coding: utf-8 -*-
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
from utils.Database import DataModel

class BusquedaWindow:
    def __init__(self, table_name, on_value_selected, search_fields={}, display_fields=[]):
        self.on_value_selected = on_value_selected
        self.model = DataModel(table_name)
        builder = gtk.Builder()
        builder.add_from_file("busqueda.glade")
        builder.connect_signals(self)
        self.window = builder.get_object("window1")
        self._search_fields = search_fields
        self.search_entry = builder.get_object("search_entry")
        self.tree = builder.get_object("treeview1")
        self.combo = builder.get_object("search_fields_combo")
        self._load_search_fields()
        self._build_treeview(display_fields)
        self.window.show()

    def _build_treeview(self, fields):
        if len(fields) == 0:
            self.column_names = self.model.get_colums()
        else:
            self.column_names = fields
        self.store = gtk.ListStore(*([str] * len(self.column_names)))
        count = 0
        for column in self.column_names:
            renderer = gtk.CellRendererText()
            label = self._get_column_label(column)
            self.tree.append_column(gtk.TreeViewColumn(label,
                renderer, text=count))
            count += 1
        self._get_data()
        self._ensure_tree_view()

    def _ensure_tree_view(self):
        self.tree.set_model(self.store)
        self.tree.show()

    def _load_search_fields(self):
        self.store_combo = gtk.ListStore(str, str)
        for key in self._search_fields.keys():
            self.store_combo.append([key, self._get_column_label(key)])
        self.combo.set_model(self.store_combo)
        self.combo.set_active(0)
        self.combo.show()

    def _get_data(self, query="", values=None):
        if len(query) == 0:
            data = self.model.get_records()
        else:
            data = self.model.get_records_from_query(query, values)
        for row in data:
            current_row = []
            for column in self.column_names:
                current_row.append(str(row[column]))
            if len(current_row) > 0:
                self.store.append(current_row)

    def _get_column_label(self, column_name):
        return column_name.replace('_', ' ').title()
    
    def on_buscar_button_clicked(self, widget):
        current_selection = self.combo.get_active()
        field = self.store_combo[current_selection][0]
        match_type = self._search_fields[field]
        value = self.search_entry.get_text()
        query = "SELECT * FROM %s WHERE %s %s ? ORDER BY %s ASC" % (self.model.table_name,
            field, ('=' if match_type == 'match' else 'like'), field)
        values = [(value if match_type == 'match' else "%%%s%%" % value)]
        model = self.tree.get_model()
        model.clear()
        self._get_data(query, values)
        self._ensure_tree_view()

    def on_cancelar_button_clicked(self, widget):
        self.window.destroy()

    def on_aceptar_btn_clicked(self, widget):
        selection = self.tree.get_selection()
        model, treeiter = selection.get_selected()
        if treeiter != None:
            index = None
            try:
                index = self.column_names.index('id')
            except:
                pass
            if index is not None and self.on_value_selected is not None:
                self.on_value_selected(model[treeiter][index])
            self.window.destroy()
        else:
            dialog = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "Debe seleccionar un registro para continuar")
            dialog.run()
            dialog.destroy()
