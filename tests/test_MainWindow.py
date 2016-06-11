import pytest
from datetime import datetime
from PyQt5 import QtCore
from models import Items


class TestMainWindow:
    """A test class for MainWindow.
    """

    @pytest.fixture
    def mainwindow(self, qtbot, mock):
        """Creates and returns a new mainwindow object, mocks its pop-up
        windows, and initialises the DB.
        """
        from lib.MainWindow import MainWindow
        import lib.extensions
        # Create the tables in an in-memory DB.
        lib.extensions.init_db()
        mainwindow = MainWindow()
        qtbot.addWidget(mainwindow)
        # msg_confirmation shows a pop-up window that is impossible to access
        # from the tests, so let's just mock it.
        mock.patch.object(MainWindow, 'msg_confirmation', return_value=True)
        return mainwindow

    @pytest.fixture
    def db(self):
        """Returns a DB session object.
        """
        from lib.extensions import db
        return db

    def test_default_values(self, mainwindow):
        """Make sure all fields contain default values.
        """
        assert mainwindow.cbItem.currentText() == '', \
            'Item field is empty by default'
        assert mainwindow.get_qty() == 1.0, \
            'Default qty/amount is 1.0'
        assert mainwindow.get_is_spending() == 1, \
            'Spending is a default operation'
        assert mainwindow.get_note() == '', \
            'Note field is empty by default'
        assert mainwindow.get_datetime().strftime('%x %X') == \
            datetime.now().strftime('%x %X'), \
            'Date and time fields show the current date and time'
        assert mainwindow.get_cost() == 0.0, \
            'Cost is 0.0 by default'
        assert mainwindow.cbLocation.currentText() == '', \
            'There are no locations yet, so the field is empty'
        assert mainwindow.cbWhere.currentText() == '', \
            'There are no users yet, so the field is empty'
        assert mainwindow.cbUnits.currentText() == '', \
            'There are no units yet, so the field is empty'
        assert mainwindow.tableView.model().rowCount() == 0, \
            'There are no expenses yet, so the balance table is empty'

    def test_add_new_item(self, qtbot, mainwindow, db):
        """Make sure we can add a new item.
        """
        new_item_name = 'New Item'
        mainwindow.cbItem.setCurrentText(new_item_name)
        qtbot.mouseClick(mainwindow.btnAdd, QtCore.Qt.LeftButton)
        assert db.query(Items).filter(
            Items.name == new_item_name).count() == 1, \
            'The item was added to the DB'
