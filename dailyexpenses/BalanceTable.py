from PyQt5.QtWidgets import QTableView
from dailyexpenses.delegators import ItemDelegator, CategoryDelegator, UserDelegator, \
    PlaceDelegator
from dailyexpenses.CustomTableModel import CustomTableModel


class BalanceTable(QTableView):

    COL_ITEMS = 0
    COL_CATEGORIES = 3
    COL_USERS = 4
    COL_PLACES = 5

    def __init__(self, parent=None):
        super(BalanceTable, self).__init__(parent)

        self.set_column_delegators({
            self.COL_ITEMS: ItemDelegator(self),
            self.COL_CATEGORIES: CategoryDelegator(self),
            self.COL_USERS: UserDelegator(self),
            self.COL_PLACES: PlaceDelegator(self),
        })
        self.setModel(CustomTableModel())
        self.show()

    def set_column_delegators(self, widgets):
        for column, widget in widgets.items():
            self.setItemDelegateForColumn(column, widget)
