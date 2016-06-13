# -*- coding: utf-8 -*-

from PyQt5 import QtGui
from PyQt5.QtSql import QSqlRelationalTableModel, QSqlRelation
from PyQt5.QtCore import Qt
from dailyexpenses.Utils import _log


class TableModel():

    def __init__(self, db):
        self.model = QSqlRelationalTableModel(db=db)

        self.model.setTable('balance')
        self.model.setEditStrategy(QSqlRelationalTableModel.OnFieldChange)
        self.model.setRelation(1, QSqlRelation('items', 'id', 'name'))
        self.model.setRelation(2, QSqlRelation('categories', 'id', 'name'))
        self.model.setRelation(4, QSqlRelation('currencies', 'id', 'name'))
        self.model.setRelation(5, QSqlRelation('users', 'id', 'full_name'))
        self.model.setRelation(6, QSqlRelation('places', 'id', 'name'))
        self.model.setRelation(8, QSqlRelation('measures', 'id', 'short'))

        self.model.setHeaderData(0, Qt.Horizontal, QtGui.qApp.tr("ID"))
        self.model.setHeaderData(1, Qt.Horizontal, QtGui.qApp.tr("Item"))
        self.model.setHeaderData(2, Qt.Horizontal, QtGui.qApp.tr("Category"))
        self.model.setHeaderData(3, Qt.Horizontal, QtGui.qApp.tr("Cost"))
        self.model.setHeaderData(4, Qt.Horizontal, QtGui.qApp.tr("Currency"))
        self.model.setHeaderData(5, Qt.Horizontal, QtGui.qApp.tr("By whom"))
        self.model.setHeaderData(6, Qt.Horizontal, QtGui.qApp.tr("Where"))
        self.model.setHeaderData(7, Qt.Horizontal, QtGui.qApp.tr("Qty/Amount"))
        self.model.setHeaderData(8, Qt.Horizontal, QtGui.qApp.tr("Units"))
        self.model.setHeaderData(9, Qt.Horizontal, QtGui.qApp.tr("is spending"))
        self.model.setHeaderData(10, Qt.Horizontal, QtGui.qApp.tr("Note"))
        self.model.setHeaderData(11, Qt.Horizontal, QtGui.qApp.tr("Date and "
                                                                  "Time"))
        self.model.removeColumn(12)
        self.model.removeColumn(13)

        if not self.model.select():
            _log("Table model selection error[%s]: %s" % (
                self.model.lastError().type(), self.model.lastError().text()
            ))

    def get_model(self):
        return self.model
