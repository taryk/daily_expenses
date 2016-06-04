# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QItemDelegate, QComboBox
from PyQt5.QtCore import Qt
from lib.Utils import _log


class ComboBoxDelegate(QItemDelegate):

    def __init__(self, parent=None, db_model=None, db_class=None,
                 show_field=None):
        super(ComboBoxDelegate, self).__init__(parent)
        self.db_model = db_model
        self.db_class = db_class
        self.show_field = show_field

    def createEditor(self, parent, option, index):
        cb_categories = QComboBox(parent)
        method_name = 'get_' + self.db_class.__tablename__
        for thing in getattr(self.db_model, method_name)():
            cb_categories.addItem(getattr(thing, self.show_field), thing.id)
        return cb_categories

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        item_index = editor.findData(value)
        _log("edit value %s. item_index %d" % (value, item_index))
        editor.setCurrentIndex(item_index)

    def setModelData(self, editor, model, index):
        data = {
            'text': editor.itemText(editor.currentIndex()),
            'extra_data': editor.itemData(editor.currentIndex()),
        }
        model.setData(index, data, Qt.EditRole)

    def _commitAndCloseEditor(self):
        editor = self.sender()
        _log("commit data")
        self.commitData.emit(editor)
        self.closeEditor.emit(editor)
        editor.deregister(True)
