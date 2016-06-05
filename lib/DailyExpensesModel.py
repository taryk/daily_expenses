# -*- coding: utf-8 -*-

from lib.Utils import _log
from lib.CustomQueryModel import CustomQueryModel
from lib.extensions import db
from models import Items, Balance


class DailyExpensesModel():

    def __init__(self, parent=None):
        self.db = db

    def get_table_view_model(self):
        return CustomQueryModel(db=self.db).get_model()

    def insert(self, data=dict()):
        try:
            new_balance_record = Balance(**data)
            self.db.add(new_balance_record)
            self.db.commit()
            return new_balance_record.id
        except Exception as e:
            _log(e)
            return

    def insert_item(self, name):
        try:
            new_item = Items(name=name)
            self.db.add(new_item)
            self.db.commit()
            return new_item.id
        except Exception as e:
            _log(e)
            return
