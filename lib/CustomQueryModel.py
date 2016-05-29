# -*- coding: utf-8 -*-

from lib.QSqlCustomQueryModel import QSqlCustomQueryModel


class CustomQueryModel():

    def __init__(self, db):
        self.model = QSqlCustomQueryModel(db=db)
        self.model.describeTable(
            table='balance',
            select=[
                {'column': ['balance', 'id']},
                {'column': ['items', 'name'], 'rel': ['item_id', 'id']},
                {'column': ['balance', 'is_spending']},
                {'column': ['balance', 'cost']},
                {'column': ['balance', 'qty']},
                {'column': ['measures', 'short'], 'rel': ['measure_id', 'id']},
                {'column': ['categories', 'name'], 'rel': ['category_id', 'id']},
                {'column': ['currencies', 'sign'], 'rel': ['currency_id', 'id']},
                {'column': ['users', 'full_name'], 'rel': ['user_id', 'id']},
                {'column': ['places', 'name'], 'rel': ['place_id', 'id']},
                {'column': ['balance', 'note']},
                {'column': ['balance', 'date']},
                {'column': ['balance', 'cdate']},
                {'column': ['balance', 'mdate']},
            ],
            order=['balance', 'date', 'DESC'],
        )
        self.model.columns(
            [
                {
                    'title': 'Item',
                    'source': lambda column: column['items_name'],
                    'edit': ['balance_item_id'],
                },
                {
                    'title': 'Cost',
                    'source': lambda column: "%s %.2f" % (
                        column['currencies_sign'],
                        (column['balance_cost'] * column['balance_is_spending'])
                    ),
                    # TODO edit currency as well
                    'edit': ['balance_cost'],
                },
                {
                    'title': 'Qty/Amount',
                    'source': lambda column: "%.2f %s" % (
                        column['balance_qty'], column['measures_short'],
                    ),
                    # TODO edit measure as well
                    'edit': ['balance_qty'],
                },
                {
                    'title': 'Category',
                    'source': lambda column: column['categories_name'],
                    'edit': ['balance_category_id'],
                },
                {
                    'title': 'By whom',
                    'source': lambda column: column['users_full_name'],
                    'edit': ['balance_user_id'],
                },
                {
                    'title': 'Where',
                    'source': lambda column: column['places_name'],
                    'edit': ['balance_place_id'],
                },
                {
                    'title': 'Date',
                    'source': lambda column: column['balance_date'],
                    # TODO edit date as well
                    'edit': None,
                },
            ]
        )

    def get_model(self):
        return self.model