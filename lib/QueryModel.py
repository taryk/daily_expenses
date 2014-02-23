# -*- coding: utf-8 -*-

from PySide import QtGui
from PySide.QtCore import Qt
from PySide.QtSql import QSqlQueryModel


class QueryModel():

    def __init__(self, db):
        self.model = QSqlQueryModel(db=db)

        self.model.setQuery(
            """
            SELECT b.id, i.name, c.sign || ' ' || (b.value * -(b.is_spending)),
            b.qty || ' ' || m.short, g.id, u.full_name, p.name, b.date
            FROM balance b
            LEFT JOIN items i ON b.item_id = i.id
            LEFT JOIN categories g ON b.category_id = g.id
            LEFT JOIN currencies c ON b.category_id = c.id
            LEFT JOIN users u ON b.user_id = u.id
            LEFT JOIN places p ON b.place_id = p.id
            LEFT JOIN measures m ON b.measure_id = m.id
            ORDER BY b.date DESC
            """)
        self.model.setHeaderData(0, Qt.Horizontal, QtGui.qApp.tr("ID"))
        self.model.setHeaderData(1, Qt.Horizontal, QtGui.qApp.tr("Item"))
        self.model.setHeaderData(2, Qt.Horizontal, QtGui.qApp.tr("Value"))
        self.model.setHeaderData(3, Qt.Horizontal, QtGui.qApp.tr("Qty/Amount"))
        self.model.setHeaderData(4, Qt.Horizontal, QtGui.qApp.tr("Category"))
        self.model.setHeaderData(5, Qt.Horizontal, QtGui.qApp.tr("By whom"))
        self.model.setHeaderData(6, Qt.Horizontal, QtGui.qApp.tr("Where"))
        self.model.setHeaderData(7, Qt.Horizontal, QtGui.qApp.tr("Date"))

    def get_model(self):
        return self.model