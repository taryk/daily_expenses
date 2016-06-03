# -*- coding: utf-8 -*-

from PyQt5 import QtGui
from PyQt5.QtSql import *
from lib.Utils import _log
from lib.CustomQueryModel import CustomQueryModel
from lib.extensions import db
from models import Items, Categories, Currencies, Locations, Places, Users, \
    Measures, Balance


class DailyExpensesModel():

    def __init__(self, parent=None):
        self.db = self.db_connect()
        self.orm_db = db

    def db_connect(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("db/daily_expenses.db")
        if not db.open():
            _log("Database opening error[%s]: %s" % (
                db.lastError().type(),
                db.lastError().text()
            ))
            QtGui.QMessageBox.critical(
                None, QtGui.qApp.tr("Cannot open database"),
                QtGui.qApp.tr("Unable to establish a database connection.\n\n"
                              "Click Cancel to exit."),
                QtGui.QMessageBox.Cancel, QtGui.QMessageBox.NoButton
            )
            return None
        return db

    def get_model(self):
        return CustomQueryModel(db=self.db).get_model()

    def insert(self, data=dict()):
        try:
            new_balance_record = Balance(**data)
            self.orm_db.add(new_balance_record)
            self.orm_db.commit()
            return new_balance_record.id
        except Exception as e:
            _log(e)
            return

    def insert_item(self, name):
        try:
            new_item = Items(name=name)
            self.orm_db.add(new_item)
            self.orm_db.commit()
            return new_item.id
        except Exception as e:
            _log(e)
            return

    def get_categories(self):
        return self.orm_db.query(Categories).all()

    def get_items(self):
        return self.orm_db.query(Items).all()

    def get_currencies(self):
        return self.orm_db.query(Currencies).all()

    def get_locations(self):
        return self.orm_db.query(Locations).all()

    def get_places(self, location_id=None):
        query = self.orm_db.query(Places)
        if location_id:
            return query.filter_by(location_id=location_id)
        return query.all()

    def get_users(self):
        return self.orm_db.query(Users).all()

    def get_measures(self):
        return self.orm_db.query(Measures).all()
