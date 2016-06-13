import random
import string
import pytest
from datetime import datetime
from sqlalchemy import String, Integer
from PyQt5 import QtCore
from models import Items, Categories, Currencies, Measures, Users, \
    Locations, Places, Balance


class TestMainWindow:
    """A test class for MainWindow.
    """

    @pytest.fixture
    def mainwindow(self, qtbot, mock):
        """Creates and returns a new mainwindow object, mocks its pop-up
        windows, and initialises the DB.
        """
        from dailyexpenses.MainWindow import MainWindow
        import dailyexpenses.extensions
        # Create the tables in an in-memory DB.
        dailyexpenses.extensions.init_db()
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
        from dailyexpenses.extensions import db
        return db

    def teardown_method(self, _):
        for model_class in (Items, Categories, Currencies, Measures,
                            Users, Locations, Places, Balance):
            model_class.db.query(model_class).delete()

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
        new_item_name = self._generate_random_string()
        mainwindow.cbItem.setCurrentText(new_item_name)
        qtbot.mouseClick(mainwindow.btnAdd, QtCore.Qt.LeftButton)
        assert db.query(Items).filter(
            Items.name == new_item_name).count() == 1, \
            'The item was added to the DB'

    def _generate_random_string(self, length=10):
        """Generates a random string with a given length.
        It uses all ascii letters (both upper and lower case) and digits.
        """
        return ''.join(random.SystemRandom().choice(
            string.ascii_letters + string.digits) for _ in range(length))

    def _generate_required_data(self, model_class):
        """Returns a dict with the bare minimum of data required to create an
        instance of a supplied model class.
        It detects required fields by checking if they can be NULL in the DB
        table model.
        """
        return {
            column.name: {
                String: lambda: self._generate_random_string(
                    column.type.length),
                Integer: lambda: 1,
            }[column.type.__class__]()
            for column in filter(
                lambda column:
                    # It's a required column.
                    not column.nullable and
                    # It's not a primary key.
                    not column.primary_key and
                    # And it's either a string or an integer.
                    isinstance(column.type, (String, Integer)),
                model_class.__table__.columns.values()
            )
        }

    def _populate(self, model_class, count=1):
        """Creates, stores, and returns a list of entities filled with random
        data.
        """
        entities = [model_class(**self._generate_required_data(model_class))
                    for _ in range(count)]
        model_class.db.add_all(entities)
        model_class.db.commit()
        return entities

    def test_entities(self, mainwindow):
        """Make sure all entities get shown correctly - they should have both
        correct titles and extra data.
        """
        for model_class in (Items, Categories, Currencies, Measures,
                            Users, Locations, Places):
            entities = self._populate(model_class, count=5)
            mainwindow.reload(model_class)
            widget = mainwindow.widgets[model_class]

            db_titles = map(lambda c: c.title(), entities)
            cb_titles = [widget.itemText(i) for i in range(widget.count())]
            assert list(db_titles) == cb_titles, \
                model_class.__singular__.title() + ' titles are the same'

            db_extra_data = map(lambda c: c.extra_data(), entities)
            cb_extra_data = [widget.itemData(i) for i in range(widget.count())]
            assert list(db_extra_data) == cb_extra_data, \
                model_class.__singular__.title() + ' extra data are the same'
