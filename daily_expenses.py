#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from datetime import datetime

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtCore import QDate, QTime, QTimer, pyqtSignal, Qt

from lib.ComboBoxDelegate import ComboBoxDelegate
from lib.DailyExpensesModel import DailyExpensesModel
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
        self.cbWhere.currentIndexChanged.connect(self.change_place)
        self.btnLocation.clicked.connect(self.change_location)

        # Timer
        self.date_timer = QTimer(self)
        self.date_timer.timeout.connect(self.date_tick)

        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.time_tick)

        self.chbCurrentDate.setCheckState(Qt.Checked)
        self.chbCurrentTime.setCheckState(Qt.Checked)

        # DB
        self.db_model = DailyExpensesModel()

        self.model = self.db_model.get_model()
        self.set_column_delegators({
            self.COL_ITEMS: ComboBoxDelegate(
               self.tableView, db=self.db_model.db, table='items'
            ),
            self.COL_CATEGORIES: ComboBoxDelegate(
                self.tableView, db=self.db_model.db, table='categories'
            ),
            self.COL_USERS: ComboBoxDelegate(
                self.tableView,
                db=self.db_model.db, table='users', data_column='full_name'
            ),
            self.COL_PLACES: ComboBoxDelegate(
                self.tableView, db=self.db_model.db, table='places'
            ),
        })

        self.tableView.setModel(self.model)
        self.tableView.show()

        self.load_data({
            'currencies': {
                'id_column': 'currency_id',
                'widget': self.cbCurrency,
                'title': '{name}',
                'extra_data': ['id', 'sign'],
            },
            'categories': {
                'id_column': 'category_id',
                'widget': self.cbCategory,
                'title': '{name}',
                'extra_data': ['id'],
            },
            'items': {
                'id_column': 'item_id',
                'widget': self.cbItem,
                'title': '{name}',
                'extra_data': ['id'],
            },
            'places': {
                'id_column': 'place_id',
                'widget': self.cbWhere,
                'title': '{name}',
                'extra_data': ['id', 'location'],
            },
            'users': {
                'id_column': 'user_id',
                'widget': self.cbByWhom,
                'title': '{full_name}',
                'extra_data': ['id'],
            },
            'measures': {
                'id_column': 'measure_id',
                'widget': self.cbUnits,
                'title': '{name} ({short})',
                'extra_data': ['id'],
            }
        })
        self.clear_fields()

    def set_column_delegators(self, widgets):
        for column, widget in widgets.items():
            self.tableView.setItemDelegateForColumn(column, widget)

    def change_currency(self):
        self.spinboxMoney.setPrefix(
            (self.cbCurrency.itemData(self.cbCurrency.currentIndex()))['sign']
            + " "
        )

    def change_place(self):
        self.btnLocation.setText(
            self.cbWhere.itemData(self.cbWhere.currentIndex())['location']
        )

    def change_location(self):
        print("click")

    def add_item(self):
        if self.validate():
            fields = [
                'item_id',    'category_id', 'user_id',  'cost', 'qty',
                'measure_id', 'is_spending', 'place_id', 'note', 'datetime',
                'currency_id'
            ]
            data = dict(zip(fields, map(self.get_value, fields)))

            self.db_model.insert(data)
            self.clear_fields()
            self.model.load_data()
        else:
            _log('failed to add')

    def get_value(self, what):
        get_value_method = 'get_' + what
        if hasattr(self, get_value_method):
            return getattr(self, get_value_method)()
        else:
            things = next(things for things in self.data_mapping.keys()
                          if self.data_mapping[things]['id_column'] == what)
            if things:
                return self.get_current_id_of(things)
            else:
                raise Exception('Unknown id_column "{:s}"'.format(what))

    def msg_confirmation(self, text, info):
        msg_box = QMessageBox()
        msg_box.setText(text)
        msg_box.setInformativeText(info)
        msg_box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard)
        msg_box.setDefaultButton(QMessageBox.Save)
        return msg_box.exec_() == QMessageBox.Save

    def get_current_id_of(self, things):
        widget = self.data_mapping[things]['widget']
        if widget:
            return widget.itemData(widget.currentIndex())['id']
        else:
            raise Exception("Unknown {:s}".format(things))

    def get_item_id(self):
        item_index = self.cbItem.findText(self.cbItem.currentText())
        if item_index >= 0:
            return self.cbItem.itemData(item_index)['id']

        if not self.msg_confirmation("Cannot find such item in DB.",
                                     "Would you like to add this one?"):
            raise Exception("don't save anything")

        item_id = self.db_model.insert_item(name=self.cbItem.currentText())
        if item_id:
            self.reload("items")
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

    def load_data(self, data_mapping):
        self.data_mapping = data_mapping
        for things, details in self.data_mapping.items():
            self._load_things(things, details)

    def _load_things(self, things, details):
        details['widget'].clear()
        stuff = getattr(self.db_model, 'get_' + things)()
        for thing in stuff:
            title = details['title'].format(**thing.__dict__)
            extra_data = dict(
                zip(
                    details['extra_data'],
                    map(lambda field: getattr(thing, field),
                        details['extra_data'])
                )
            )
            details['widget'].addItem(title, extra_data)

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
