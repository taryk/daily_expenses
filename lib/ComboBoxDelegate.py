# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QItemDelegate, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery
from lib.Utils import _log


class ComboBoxDelegate(QItemDelegate):

    def __init__(self, parent=None, db=None, table=None, id_column='id',
                 data_column='name'):
        super(ComboBoxDelegate, self).__init__(parent)
        self.db = db
        self.table = table
        self.id_column = id_column
        self.data_column = data_column

    def createEditor(self, parent, option, index):
        cb_categories = QComboBox(parent)
        select_query = QSqlQuery(db=self.db)
        query = 'SELECT %s, %s FROM %s ORDER BY %s' % (
            self.id_column, self.data_column, self.table, self.id_column
        )
        if not select_query.exec_(query):
            _log("Selection error[%s]: %s" % (
                select_query.lastError().type(),
                select_query.lastError().text()
            ))
        while select_query.next():
            record = select_query.record()
            cb_categories.addItem(
                record.value(self.data_column),
                record.value(self.id_column)
            )
        return cb_categories

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        item_index = editor.findData(value)
        _log("edit value %s. item_index %d" % (value, item_index))
        editor.setCurrentIndex(item_index)

    def setModelData(self, editor, model, index):
        data = {
            self.table + '_' + self.id_column: editor.itemData(
                editor.currentIndex()
            ),
            self.table + '_' + self.data_column: editor.itemText(
                editor.currentIndex()
            ),
        }
        _log("set data %s" % data)
        model.setData(index, data, Qt.EditRole)

    def _commitAndCloseEditor(self):
        editor = self.sender()
        _log("commit data")
        self.commitData.emit(editor)
        self.closeEditor.emit(editor)
        editor.deregister(True)