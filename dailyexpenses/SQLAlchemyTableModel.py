# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractTableModel
from models import Balance
from dailyexpenses.extensions import db


class SQLAlchemyTableModel(QAbstractTableModel):

    def __init__(self, parent=None):
        super(SQLAlchemyTableModel, self).__init__(parent)
        self.db = db
        self.columns = []
        self.table_data = []

    def describe_columns(self, columns=[]):
        self.columns = columns
        for column in columns:
            self.setHeaderData(0, QtCore.Qt.Horizontal, column['title'])

    def load_data(self):
        self.table_data = Balance.all()

    def rowCount(self, _parent=QtCore.QModelIndex()):
        # return self.select_query.result().size()
        # FIXME after adding new record this value stays the same
        return len(self.table_data)

    def columnCount(self, _parent=QtCore.QModelIndex()):
        return len(self.columns)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        column = self.columns[index.column()]
        if role == QtCore.Qt.EditRole and column['edit']:
            return column['edit'](self.table_data[index.row()])
        elif role == QtCore.Qt.DisplayRole:
            return column['source'](self.table_data[index.row()])
        return None

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.columns[section]['title']
            else:
                return self.table_data[section].id
        return None

    def insertRows(self, row, count, parent=QtCore.QModelIndex()):
        for i in range(row, row + count):
            self.insertRow(i)
        return True

    def insertRow(self, row, parent=QtCore.QModelIndex()):
        QtCore.QAbstractTableModel.beginInsertRows(self, parent, row, row)
        self.table_data[row] = Balance()
        QtCore.QAbstractTableModel.endInsertRows(self)
        return True

    def removeRow(self, row, parent=QtCore.QModelIndex()):
        QtCore.QAbstractTableModel.beginRemoveRows(self, parent, row, row)
        self.table_data.remove(row)
        # TODO remove from db table
        QtCore.QAbstractTableModel.endRemoveRows(self)
        return True

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        for i in range(row, row + count):
            self.removeRow(i)
        return True

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        column = self.columns[index.column()]
        if column['edit']:
            print(index.column(), value)
            if type(value) == dict:
                column['set'](self.table_data[index.row()],
                              value['extra_data'])
            else:
                column['set'](self.table_data[index.row()], value)
            self.db.commit()
            return True
        return False

    def flags(self, index):
        flags = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        if self.columns[index.column()]['edit']:
            flags |= QtCore.Qt.ItemIsEditable
        return flags
