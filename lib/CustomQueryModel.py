# -*- coding: utf-8 -*-

from lib.SQLAlchemyTableModel import SQLAlchemyTableModel


class CustomQueryModel:

    def __init__(self):
        self.model = SQLAlchemyTableModel()
        self.model.load_data()
        self.model.describe_columns(
            [
                {
                    'title': 'Item',
                    'source': lambda balance: balance.item.name,
                    'edit': lambda balance: balance.item_id,
                    'set': lambda balance, value: setattr(balance, 'item_id',
                                                          value),
                },
                {
                    'title': 'Cost',
                    'source': lambda balance: '{:s} {:.2f}'.format(
                        balance.currency.sign,
                        balance.cost * balance.is_spending
                    ),
                    # TODO edit currency as well
                    'edit': lambda balance: balance.cost,
                    'set': lambda balance, value: setattr(balance, 'cost',
                                                          value),
                },
                {
                    'title': 'Qty/Amount',
                    'source': lambda balance: "{:.2f} {:s}".format(
                        balance.qty, balance.measure.short,
                    ),
                    # TODO edit measure as well
                    'edit': lambda balance: balance.qty,
                    'set': lambda balance, value: setattr(balance, 'qty',
                                                          value),
                },
                {
                    'title': 'Category',
                    'source': lambda balance: balance.category.name,
                    'edit': lambda balance: balance.category_id,
                    'set': lambda balance, value: setattr(balance,
                                                          'category_id',
                                                          value),
                },
                {
                    'title': 'By whom',
                    'source': lambda balance: balance.user.full_name,
                    'edit': lambda balance: balance.user_id,
                    'set': lambda balance, value: setattr(balance, 'user_id',
                                                          value),
                },
                {
                    'title': 'Where',
                    'source': lambda balance: balance.place.name,
                    'edit': lambda balance: balance.place_id,
                    'set': lambda balance, value: setattr(balance, 'place_id',
                                                          value),
                },
                {
                    'title': 'Date and Time',
                    'source': lambda balance: balance.datetime.isoformat(' '),
                    # TODO edit date as well
                    'edit': None,
                    'set': None,
                },
            ]
        )

    def get_model(self):
        return self.model
