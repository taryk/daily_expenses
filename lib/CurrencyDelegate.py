# -*- coding: utf-8 -*-

from PyQt5.QtWidget import QItemDelegate


class CurrencyDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(QItemDelegate, self).__init__(parent)
