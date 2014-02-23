# -*- coding: utf-8 -*-

from PySide import QtCore
from PySide.QtSql import QSqlQuery
from PySide.QtCore import QAbstractTableModel


class QSqlCustomQueryModel(QAbstractTableModel):

    def __init__(self, parent=None, db=None):
        super(QSqlCustomQueryModel, self).__init__(parent)
        self.db = db
        self.select_query = QSqlQuery(db=self.db)
        self._columns = []
        self._data = []
        self.select_columns = []
        self.query = None

    def describeTable(self, table=None, select=None, order=None):
        joins = []
        for item in select:
            self.select_columns.append(
                item['column'][0] + '.' + item['column'][1]
            )
            if 'rel' in item:
                self.select_columns.append(table + '.' + item['rel'][0])
                joins.append('LEFT JOIN %s ON %s.%s = %s.%s' % (
                    item['column'][0],
                    table, item['rel'][0],
                    item['column'][0], item['rel'][1],
                ))
        self.query = "SELECT %s FROM %s %s ORDER BY %s.%s %s" % (
            ','.join(map(
                lambda x: x + ' AS ' + x.replace('.', '_'),
                self.select_columns)),
            table,
            ' '.join(joins),
            order[0], order[1], order[2]
        )

        self.load_data()

    def load_data(self):
        self._data = []

        if not self.select_query.exec_(self.query):
            print("QSqlCustomQueryModel selection error [%s]: %s" % (
                self.select_query.lastError().type(),
                self.select_query.lastError().text()
            ))

        while self.select_query.next():
            row = {}
            record = self.select_query.record()
            for col in self.select_columns:
                col_name = col.replace('.', '_')
                row[col_name] = record.value(col_name)
            self._data.append(row)

    def columns(self, cols=[]):
        self._columns = cols
        for col in cols:
            self.setHeaderData(0, QtCore.Qt.Horizontal, col['title'])

    def rowCount(self, _parent=QtCore.QModelIndex()):
        # return self.select_query.result().size()
        # FIXME after adding new record this value stays the same
        return len(self._data)

    def columnCount(self, _parent=QtCore.QModelIndex()):
        return len(self._columns)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        col = self._columns[index.column()]
        if role == QtCore.Qt.EditRole and col['edit']:
            return self._data[index.row()][col['edit'][0]]
        elif role == QtCore.Qt.DisplayRole:
            return col['source'](self._data[index.row()])
        return None

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._columns[section]['title']
            else:
                return self._data[section]['balance_id']
        return None

    def insertRows(self, row, count, parent=QtCore.QModelIndex()):
        for i in range(row, row + count):
            self.insertRow(i)
        return True

    def insertRow(self, row, parent=QtCore.QModelIndex()):
        empty_data = {}
        for column in self.select_columns:
            empty_data[column] = None
        QtCore.QAbstractTableModel.beginInsertRows(self, parent, row, row)
        self._data[row] = empty_data
        QtCore.QAbstractTableModel.endInsertRows(self)
        return True

    def removeRow(self, row, parent=QtCore.QModelIndex()):
        QtCore.QAbstractTableModel.beginRemoveRows(self, parent, row, row)
        self._data.remove(row)
        # TODO remove from db table
        QtCore.QAbstractTableModel.endRemoveRows(self)
        return True

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        for i in range(row, row + count):
            self.removeRow(i)
        return True

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        col = self._columns[index.column()]
        if col['edit']:
            print(index.column(), value)
            # TODO update db table
            if type(value) == dict:
                for column in value:
                    self._data[index.row()][column] = value[column]
            else:
                self._data[index.row()][col['edit'][0]] = value
            return True
        return False

    def flags(self, index):
        flags = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        if self._columns[index.column()]['edit']:
            flags |= QtCore.Qt.ItemIsEditable
        return flags
