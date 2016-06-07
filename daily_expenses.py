#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from datetime import datetime

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtCore import QDate, QTime, QTimer, pyqtSignal, Qt

from lib.CustomTableModel import CustomTableModel
from lib.delegators import ItemDelegator, CategoryDelegator, UserDelegator, \
    PlaceDelegator
from models import Balance, Items, Categories, Currencies, Places, \
    Locations, Measures, Users
from lib.Utils import _log
from ui.ui_dailyexpenses import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    COL_ITEMS = 0
    COL_CATEGORIES = 3
    COL_USERS = 4
    COL_PLACES = 5

    data_mapping = {}

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.btnAdd.clicked.connect(self.add_item)
        self.chbCurrentDate.toggled.connect(self.current_date)
        self.chbCurrentTime.toggled.connect(self.current_time)
        self.cbCurrency.currentIndexChanged.connect(self.change_currency)
        self.cbLocation.currentIndexChanged.connect(self.change_location)

        # Timer
        self.date_timer = QTimer(self)
        self.date_timer.timeout.connect(self.date_tick)

        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.time_tick)

        self.chbCurrentDate.setCheckState(Qt.Checked)
        self.chbCurrentTime.setCheckState(Qt.Checked)

        self.table_view_model = CustomTableModel()
        self.set_column_delegators({
            self.COL_ITEMS: ItemDelegator(self.tableView),
            self.COL_CATEGORIES: CategoryDelegator(self.tableView),
            self.COL_USERS: UserDelegator(self.tableView),
            self.COL_PLACES: PlaceDelegator(self.tableView),
        })

        self.tableView.setModel(self.table_view_model)
        self.tableView.show()

        self.load_data(
            [Currencies, self.cbCurrency],
            [Categories, self.cbCategory],
            [Items,      self.cbItem],
            [Locations,  self.cbLocation],
            [Places,     self.cbWhere],
            [Users,      self.cbByWhom],
            [Measures,   self.cbUnits],
        )
        self.clear_fields()

    def set_column_delegators(self, widgets):
        for column, widget in widgets.items():
            self.tableView.setItemDelegateForColumn(column, widget)

    def change_currency(self):
        self.spinboxMoney.setPrefix(
            (self.cbCurrency.itemData(self.cbCurrency.currentIndex()))['sign']
            + " "
        )

    def change_location(self):
        self.reload(Places)

    def add_item(self):
        if self.validate():
            fields = [
                'item_id',    'category_id', 'user_id',  'cost', 'qty',
                'measure_id', 'is_spending', 'place_id', 'note', 'datetime',
                'currency_id'
            ]
            data = dict(zip(fields, map(self.get_value, fields)))

            Balance.insert(data)
            self.clear_fields()
            self.table_view_model.load_data()
        else:
            _log('failed to add')

    def get_value(self, what):
        get_value_method = 'get_' + what
        if hasattr(self, get_value_method):
            return getattr(self, get_value_method)()
        else:
            model_class = next(
                model_class for model_class in self.data_mapping.keys()
                if model_class.__singular__ + '_id' == what
            )
            if model_class:
                return self.get_current_id_of(model_class)
            else:
                raise Exception('Unknown id_column "{:s}"'.format(what))

    def msg_confirmation(self, text, info):
        msg_box = QMessageBox()
        msg_box.setText(text)
        msg_box.setInformativeText(info)
        msg_box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard)
        msg_box.setDefaultButton(QMessageBox.Save)
        return msg_box.exec_() == QMessageBox.Save

    def get_current_id_of(self, model_class):
        widget = self.data_mapping[model_class]
        if widget:
            return widget.itemData(widget.currentIndex())['id']
        else:
            raise Exception("Unknown {:s}".format(model_class))

    def get_item_id(self):
        item_index = self.cbItem.findText(self.cbItem.currentText())
        if item_index >= 0:
            return self.cbItem.itemData(item_index)['id']

        if not self.msg_confirmation("Cannot find such item in DB.",
                                     "Would you like to add this one?"):
            raise Exception("don't save anything")

        item_id = Items.insert(name=self.cbItem.currentText())
        if item_id:
            self.reload(Items)
            return item_id
        else:
            return None

    def get_qty(self):
        return self.spinboxQty.value()

    def get_is_spending(self):
        return self.rbExpense.isChecked() and 1 or 0

    def get_note(self):
        return self.textNote.toPlainText()

    def get_cost(self):
        return self.spinboxMoney.value()

    def get_datetime(self):
        return datetime.combine(self.dateEdit.date().toPyDate(),
                                self.timeEdit.time().toPyTime())

    def date_tick(self):
        self.dateEdit.setDate(QDate.currentDate())

    def time_tick(self):
        self.timeEdit.setTime(QTime.currentTime())

    def current_date(self):
        current = self.chbCurrentDate.isChecked()
        if current:
            self.date_tick()
            self.date_timer.start(1000)
        else:
            self.date_timer.stop()
        self.dateEdit.setEnabled(not current)

    def current_time(self):
        current = self.chbCurrentTime.isChecked()
        if current:
            self.time_tick()
            self.time_timer.start(1000)
        else:
            self.time_timer.stop()
        self.timeEdit.setEnabled(not current)

    def validate(self):
        if len(self.cbItem.lineEdit().text()) == 0:
            _log('item cannot be null')
            return False
        if len(self.cbCategory.lineEdit().text()) == 0:
            _log('category cannot be null')
            return False
        if len(self.cbWhere.lineEdit().text()) == 0:
            _log('place cannot be null')
            return False
        if len(self.cbByWhom.lineEdit().text()) == 0:
            _log('who cannot be null')
            return False
        return True

    def load_data(self, *data_mapping):
        for details in data_mapping:
            self.data_mapping[details[0]] = details[1]
        for details in data_mapping:
            self._load_things(*details)

    def _load_things(self, model_class, widget):
        widget.clear()
        args = dict()
        for depend_on in model_class.__depend_on__:
            id_column = depend_on.__singular__ + '_id'
            args[id_column] = self.get_current_id_of(depend_on)

        stuff = model_class.all(**args)
        for thing in stuff:
            widget.addItem(thing.title(), thing.extra_data())

    def reload(self, things):
        self._load_things(things, self.data_mapping[things])

    def clear_fields(self):
        self.spinboxMoney.setValue(0.0)
        self.spinboxQty.setValue(1.0)
        self.cbItem.setCurrentIndex(-1)
        self.spinboxQty.setValue(1.0)
        self.cbUnits.setCurrentIndex(0)
        # self.cbCategory.setCurrentIndex(-1)
        # self.cbWhere.setCurrentIndex(-1)
        # self.cbByWhom.setCurrentIndex(-1)
        self.textNote.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
