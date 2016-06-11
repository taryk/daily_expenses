from datetime import datetime

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import QDate, QTime, QTimer, Qt

from models import Balance, Items, Categories, Currencies, Places, \
    Locations, Measures, Users
from lib.Utils import _log
from ui.ui_dailyexpenses import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.widgets = dict()
        self.load_data(
            [Currencies, self.cbCurrency],
            [Categories, self.cbCategory],
            [Items,      self.cbItem],
            [Locations,  self.cbLocation],
            [Places,     self.cbWhere],
            [Users,      self.cbByWhom],
            [Measures,   self.cbUnits],
        )

        self.btnAdd.clicked.connect(self.add_balance_record)
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

        self.clear_fields()

    def change_currency(self):
        self.spinboxMoney.setPrefix(
            (self.cbCurrency.itemData(self.cbCurrency.currentIndex()))['sign']
            + " "
        )

    def change_location(self):
        self.reload(Places)

    def add_balance_record(self):
        fields = [
            'item_id',    'category_id', 'user_id',  'cost', 'qty',
            'measure_id', 'is_spending', 'place_id', 'note', 'datetime',
            'currency_id'
        ]
        try:
            data = dict(zip(fields, map(self.get_value, fields)))
            Balance.insert(data)
        except Exception as e:
            _log("Can't add a record.", e)
            return
        self.clear_fields()
        self.tableView.model().load_data()

    def get_value(self, entity):
        get_value_method = 'get_' + entity
        if hasattr(self, get_value_method):
            return getattr(self, get_value_method)()
        else:
            model_class = next(
                model_class for model_class in self.widgets.keys()
                if model_class.__singular__ + '_id' == entity
            )
            if model_class:
                return self.get_current_id_of(model_class)
            else:
                raise Exception('Unknown entity "{:s}".'.format(entity))

    def msg_confirmation(self, text, info):
        msg_box = QMessageBox()
        msg_box.setText(text)
        msg_box.setInformativeText(info)
        msg_box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard)
        msg_box.setDefaultButton(QMessageBox.Save)
        return msg_box.exec_() == QMessageBox.Save

    def get_current_id_of(self, model_class):
        widget = self.widgets[model_class]
        if widget is not None:
            if widget.currentIndex() < 0:
                return None
            return widget.itemData(widget.currentIndex())['id']
        else:
            raise Exception("Unknown entity {:s}.".format(model_class.__name__))

    def get_item_id(self):
        item_index = self.cbItem.findText(self.cbItem.currentText())
        if item_index >= 0:
            return self.cbItem.itemData(item_index)['id']

        if not self.msg_confirmation("Cannot find such an item in the DB.",
                                     "Would you like to add this one?"):
            return None

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

    def load_data(self, *class_widget_list):
        for details in class_widget_list:
            self.widgets[details[0]] = details[1]
            self._load_entities(*details)

    def _load_entities(self, model_class, widget):
        widget.clear()
        args = dict()
        for depend_on in model_class.__depend_on__:
            id_column = depend_on.__singular__ + '_id'
            args[id_column] = self.get_current_id_of(depend_on)

        entities = model_class.all(**args)
        for entity in entities:
            widget.addItem(entity.title(), entity.extra_data())

    def reload(self, model_class):
        self._load_entities(model_class, self.widgets[model_class])

    def clear_fields(self):
        self.spinboxMoney.setValue(0.0)
        self.spinboxQty.setValue(1.0)
        self.cbItem.setCurrentIndex(-1)
        self.spinboxQty.setValue(1.0)
        self.cbUnits.setCurrentIndex(0)
        self.textNote.clear()
