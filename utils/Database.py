import sqlite3
import re

class DbConnection:
    class __implementation:
        def __init__(self):
            self.connection = sqlite3.connect('pv.db')

        def close(self):
            self.connection.close()

        def cursor(self):
            return self.connection.cursor()

        def commit(self):
            self.connection.commit()

    __instance = None

    def __init__(self):
        if DbConnection.__instance is None:
            DbConnection.__instance = DbConnection.__implementation()
        self.__dict__['_DbConnection__instance'] = DbConnection.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)


    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)

class DataModel:
    __columns = []

    def __init__(self, table_name):
        self.table_name = table_name
        self.db = DbConnection()
        self.__set_columns()

    def __set_columns(self):
        cursor = self.db.cursor()
        cursor.execute("PRAGMA table_info('%s')" % self.table_name) 
        self.__columns = [str(row[1]) for row in cursor]
        cursor.close()

    def get_colums(self):
        return self.__columns

    def get_record(self, record_id):
        self.db.connection.row_factory = sqlite3.Row
        cursor = self.db.cursor()
        query = "SELECT %s FROM %s WHERE id = %d"\
            % (','.join(self.__columns), self.table_name, record_id)
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        return row

    def get_records(self, *args, **kwargs):
        query = 'SELECT * FROM %s' % self.table_name
        values = None
        if len(kwargs) > 0:
            fields = [x  for x in kwargs.keys()]
            values = [y for y in kwargs.values()]
            query += ' WHERE ' + ' = ? AND '.join(fields) + ' = ?'
        rows = self.get_records_from_query(query, values)
        return rows
    
    def get_records_from_query(self, query, values=None):
        self.db.connection.row_factory = sqlite3.Row
        cursor = self.db.cursor()
        if values is not None:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def delete_record(self, record_id):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM %s WHERE id = %d"\
            % (self.table_name, record_id))
        cursor.close()

    def create_record(self, fields_and_values):
        if len(fields_and_values) > 0:
            fields = [x for x in fields_and_values.keys()]
            values = [y.decode('utf-8') for y in fields_and_values.values()]
            values_count = ['?' for x in fields_and_values.keys()]
            cursor = self.db.cursor()
            query = "INSERT INTO %s(%s) values(%s)" % (self.table_name, ', '.join(fields), ', '.join(values_count))
            cursor.execute(query, values)
            self.db.commit()
            cursor.close()

    def update_record(self, fields_and_values, record_id):
        if len(fields_and_values) > 0:
            fields = [x for x in fields_and_values.keys()]
            values = [y.decode('utf-8') for y in fields_and_values.values()]
            query = "UPDATE %s SET %s WHERE id = %d" % (self.table_name, ' = ?, '.join(fields) + ' = ?', 
                record_id)
            cursor = self.db.cursor()
            cursor.execute(query, values)
            self.db.commit()
            cursor.close()

    def dispose(self):
        self.db.close()
