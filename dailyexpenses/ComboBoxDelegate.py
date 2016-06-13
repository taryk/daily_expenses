# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QItemDelegate, QComboBox
from PyQt5.QtCore import Qt
from dailyexpenses.Utils import _log


class ComboBoxDelegate(QItemDelegate):

    def __init__(self, parent=None, model_class=None, show_field=None):
        super(ComboBoxDelegate, self).__init__(parent)
        self.model_class = model_class
        self.show_field = show_field

    def createEditor(self, parent, option, index):
        combobox = QComboBox(parent)
        for entity in self.model_class.all():
            combobox.addItem(getattr(entity, self.show_field), entity.id)
        return combobox

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
