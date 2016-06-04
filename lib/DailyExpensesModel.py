# -*- coding: utf-8 -*-

from lib.Utils import _log
from lib.CustomQueryModel import CustomQueryModel
from lib.extensions import db
from models import Items, Categories, Currencies, Locations, Places, Users, \
    Measures, Balance


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

    def get_categories(self):
        return self.db.query(Categories).all()

    def get_items(self):
        return self.db.query(Items).all()

    def get_currencies(self):
        return self.db.query(Currencies).all()

    def get_locations(self):
        return self.db.query(Locations).all()

    def get_places(self, location_id=None):
        query = self.db.query(Places)
        if location_id:
            return query.filter_by(location_id=location_id)
        return query.all()

    def get_users(self):
        return self.db.query(Users).all()

    def get_measures(self):
        return self.db.query(Measures).all()
