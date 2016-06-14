import random
import string
import pytest
from datetime import datetime
from sqlalchemy import String, Integer
from PyQt5 import QtCore
from dailyexpenses.DataBase import DataBase
from models import Items, Categories, Currencies, Measures, Users, \
    Locations, Places, Balance


class TestMainWindow:
    """A test class for MainWindow.
    """

    def setup_class(self):
        """Just creates a new DB instance at the beginning of the test class.
        """
        self.db = DataBase()

    def teardown_method(self, _):
        """Clear all tables.
        """
        for model_class in (Items, Categories, Currencies, Measures,
                            Users, Locations, Places, Balance):
            self.db.query(model_class).delete()

    @pytest.fixture
    def mainwindow(self, qtbot, mock):
        """Creates and returns a new mainwindow object, mocks its pop-up
        windows, and initialises the DB.
        """
        from dailyexpenses.MainWindow import MainWindow
        # Create the tables in an in-memory DB.
        DataBase.create_tables()
        mainwindow = MainWindow()
        qtbot.addWidget(mainwindow)
        # msg_confirmation shows a pop-up window that is impossible to access
        # from the tests, so let's just mock it.
        mock.patch.object(MainWindow, 'msg_confirmation', return_value=True)
        return mainwindow

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

    def test_add_new_item(self, qtbot, mock, mainwindow):
        """Make sure we can add a new item.
        """
        new_item_name = self._generate_random_string()
        test_cases = [
            {
                'title': 'The item has not been added to the DB',
                'msg_confirmation': False,
                'items_matched': 0
            },
            {
                'title': 'The item was added to the DB',
                'msg_confirmation': True,
                'items_matched': 1
            },
        ]
        for test_case in test_cases:
            mainwindow.cbItem.setCurrentText(new_item_name)
            mock.patch.object(mainwindow, 'msg_confirmation',
                              return_value=test_case['msg_confirmation'])
            qtbot.mouseClick(mainwindow.btnAdd, QtCore.Qt.LeftButton)
            assert self.db.query(Items).filter(
                Items.name == new_item_name
            ).count() == test_case['items_matched'], test_case['title']
            assert mainwindow.cbItem.currentText() == '', \
                'Item field gets cleared'

    def test_add_new_balance_record(self, qtbot, mainwindow):
        """Make sure we can add a new balance record.
        """
        values = {
            Balance.cost: 153.32,
            Balance.qty: 11,
            Balance.note: ' '.join(
                map(lambda _: self._generate_random_string(), range(10))
            )
        }
        for model_class in (Items, Categories, Currencies, Measures,
                            Users, Locations, Places):
            predefined_data = dict()
            for depend_on in model_class.__depend_on__:
                predefined_data[depend_on.foreign_column_name()] = \
                    mainwindow.get_current_id_of(depend_on)

            entities = self._populate(model_class, predefined_data, count=2)
            attribute_name = model_class.foreign_column_name()
            if hasattr(Balance, attribute_name):
                balance_attribute = getattr(Balance, attribute_name)
                values[balance_attribute] = entities[1].id
            mainwindow.reload(model_class)
            mainwindow.widgets[model_class].setCurrentIndex(1)

        mainwindow.spinboxMoney.setValue(values[Balance.cost])
        mainwindow.spinboxQty.setValue(values[Balance.qty])
        mainwindow.textNote.setPlainText(values[Balance.note])
        qtbot.mouseClick(mainwindow.btnAdd, QtCore.Qt.LeftButton)
        query = self.db.query(Balance)
        for column, value in values.items():
            query = query.filter(column == value)
        assert query.count() == 1, \
            'The expense record has been added to the DB'

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
        def _get_column_value(column):
            return {
                String: lambda: self._generate_random_string(
                    column.type.length),
                Integer: lambda: 1,
            }[column.type.__class__]()

        return {
            column.name: _get_column_value(column)
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

    def _populate(self, model_class, predefined_data=dict(), count=1):
        """Creates, stores, and returns a list of entities filled with randomly
        generated and/or predefined data.
        """
        def required_data():
            """Merges randomly generated data with predefined one.
            """
            return {
                # Generate a bare minimum of required data.
                **self._generate_required_data(model_class),
                # If there are any predefined values, include them too.
                **predefined_data
            }

        entities = [model_class(**required_data()) for _ in range(count)]
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
