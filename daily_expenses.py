#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtCore import QDate, QTime, QTimer, pyqtSignal, Qt

sys.path.append('lib')

from lib.ComboBoxDelegate import ComboBoxDelegate
from lib.DailyExpensesModel import DailyExpensesModel
from lib.Utils import _log
from ui.ui_dailyexpenses import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    COL_ITEMS = 0
    COL_CATEGORIES = 3
    COL_USERS = 4
    COL_PLACES = 5

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.btnAdd.clicked.connect(self.add_item)
        self.chbCurrentDate.toggled.connect(self.current_date)
        self.chbCurrentTime.toggled.connect(self.current_time)
        self.cbCurrency.currentIndexChanged.connect(self.change_currency)

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
        self.tableView.setItemDelegateForColumn(
            self.COL_ITEMS, ComboBoxDelegate(
                self.tableView, db=self.db_model.db, table='items'
            )
        )
        self.tableView.setItemDelegateForColumn(
            self.COL_CATEGORIES, ComboBoxDelegate(
                self.tableView, db=self.db_model.db, table='categories'
            )
        )
        self.tableView.setItemDelegateForColumn(
            self.COL_USERS, ComboBoxDelegate(
                self.tableView,
                db=self.db_model.db, table='users', data_column='full_name'
            )
        )
        self.tableView.setItemDelegateForColumn(
            self.COL_PLACES, ComboBoxDelegate(
                self.tableView, db=self.db_model.db, table='places'
            )
        )

        self.tableView.setModel(self.model)
        self.tableView.show()

        # Load data
        self.load_currencies()
        self.load_categories()
        self.load_items()
        self.load_users()
        self.load_places()
        self.load_measures()

        self.clear_fields()

    def change_currency(self):
        self.spinboxMoney.setPrefix(
            (self.cbCurrency.itemData(self.cbCurrency.currentIndex()))['sign']
            + " "
        )

    def add_item(self):
        if self.validate():
            self.db_model.insert(
                {
                    'item_id': self.get_item_id(),
                    'category_id': self.get_category_id(),
                    'cost': self.get_cost(),
                    'currency_id': self.get_currency_id(),
                    'user_id': self.get_user_id(),
                    'place_id': self.get_place_id(),
                    'qty': self.get_qty(),
                    'measure_id': self.get_measure_id(),
                    'is_spending': self.is_spending(),
                    'note': self.get_note(),
                    'date': self.get_datetime(),
                }
            )
            self.clear_fields()
            self.model.load_data()
        else:
            _log('failed to add')

    def msg_confirmation(self, text, info):
        msg_box = QMessageBox()
        msg_box.setText(text)
        msg_box.setInformativeText(info)
        msg_box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard)
        msg_box.setDefaultButton(QMessageBox.Save)
        return msg_box.exec_() == QMessageBox.Save

    def get_item_id(self):
        item_index = self.cbItem.findText(self.cbItem.currentText())
        if item_index >= 0:
            return self.cbItem.itemData(item_index)

        if not self.msg_confirmation("Cannot find such item in DB.",
                                     "Would you like to add this one?"):
            raise Exception("don't save anything")

        self.db_model.insert_item(name=self.cbItem.currentText())
        item_id = self.db_model.get_item_id(name=self.cbItem.currentText())
        if item_id:
            self.load_items()
            return item_id
        else:
            return None

    def get_category_id(self):
        return self.cbCategory.itemData(self.cbCategory.currentIndex())

    def get_currency_id(self):
        return (self.cbCurrency.itemData(self.cbCurrency.currentIndex()))['id']

    def get_user_id(self):
        return self.cbByWhom.itemData(self.cbByWhom.currentIndex())

    def get_place_id(self):
        return self.cbWhere.itemData(self.cbWhere.currentIndex())

    def get_qty(self):
        return self.spinboxQty.value()

    def get_measure_id(self):
        return self.cbUnits.itemData(self.cbUnits.currentIndex())

    def is_spending(self):
        return self.rbSpending.isChecked() and 1 or 0

    def get_note(self):
        return self.textNote.toPlainText()

    def get_cost(self):
        return self.spinboxMoney.value()

    def get_datetime(self):
        return(self.dateEdit.date().toString("yyyy.MM.dd") + " " +
               self.timeEdit.time().toString("hh:mm:ss"))

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

    # TODO all load_* methods look similar. Try to follow DRY
    def load_currencies(self):
        self.cbCurrency.clear()
        for currency in self.db_model.get_currencies():
            self.cbCurrency.addItem(
                currency['name'],
                {
                    'id': currency['id'],
                    'sign': currency['sign']
                }
            )

    def load_categories(self):
        self.cbCategory.clear()
        for category in self.db_model.get_categories():
            self.cbCategory.addItem(category['name'], category['id'])

    def load_items(self):
        self.cbItem.clear()
        for item in self.db_model.get_items():
            self.cbItem.addItem(item['name'], item['id'])

    def load_places(self):
        self.cbWhere.clear()
        for place in self.db_model.get_places():
            self.cbWhere.addItem(
                '%s (%s)' % (place['name'], place['location']),
                place['id']
            )

    def load_users(self):
        self.cbByWhom.clear()
        for user in self.db_model.get_users():
            self.cbByWhom.addItem(user['full_name'], user['id'])

    def load_measures(self):
        self.cbUnits.clear()
        for measure in self.db_model.get_measures():
            self.cbUnits.addItem(
                '%s (%s)' % (measure['name'], measure['short']),
                measure['id']
            )

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
